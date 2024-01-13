from django.shortcuts import render, redirect
from .models import Post, Ingred, RecipeIngred, RecipeDetail, Rating
from .forms import PostForm, RatingForm
from django.contrib.auth.decorators import login_required
import logging
from django.db.models import Q, Sum, Avg
from .recommened_ml import recommend_recipe
from .item_collabs import load_user_recom2
from datetime import datetime
from .time_sort import time_recommend,user_recommend2
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
import json, os, shutil
from django.contrib import messages

# settings.py 파일에서 설정된 로거를 취득
import logging 
logger = logging.getLogger('file2')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def index(request):
    # order_by('-id') 최근에 생성된 게시물이 위에 보여지도록!
    posts = Post.objects.all().order_by('-id')
    user_id = request.user
    ## 시간대별 레시피 추천
    current_time = datetime.now().hour
    file_path = '/home/ubuntu/web/recipe_web/logsfolder/json_log.log'
    if 5 <= current_time < 10:
        time_label = '아침'
    elif 10 <= current_time < 16:
        time_label = '점심'
    elif 16 <= current_time < 23:
        time_label = '저녁'
    else:
        time_label = '새벽'
    recommend_list = time_recommend(file_path, time_label)
    score_based_user_recom_list = load_user_recom2(user_id.id)
    if score_based_user_recom_list == '별점 없음':
        score_based_user_recom_posts = []
    else:
        score_based_user_recom_posts = Post.objects.filter(id__in=score_based_user_recom_list)
    time_posts = Post.objects.filter(id__in=recommend_list[:4])
    age = request.user.age // 10 * 10
    sex = request.user.sex
    user_recommend_list = user_recommend2(age,sex)
    user_posts = Post.objects.filter(id__in=user_recommend_list[:4])
    context = {
        'posts': posts,
        'user_id': user_id,
        'index': '이런 레시피들은 어때요?',
        'time_posts': time_posts,
        'time_label': time_label, 
        'age': age,
        'sex': sex,
        'score_based_user_recom_posts': score_based_user_recom_posts,
        'user_posts': user_posts,   
    }
    return render(request, 'index_main.html', context)

def hit(request):
    posts_hit = Post.objects.filter(post_hit__gt=0).order_by('-post_hit')
    return render(request, 'index_hit.html', {'posts_hit': posts_hit})

def score(request): 
    # annotate 함수를 통해 각 게시물의 별점 평균 계산
    posts_score = Post.objects.annotate(avg_score=Avg('ratings__score')).order_by('-avg_score')
    return render(request, 'index_score.html', {'posts_score': posts_score})

def create_by_img(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        files = {'image': (image_file.name, image_file.read())}
        
        flask_response = requests.post('보안상삭제', files=files)
        ingred_create_list = json.loads(flask_response.text, encoding="UTF-8").get('ingred_create')
        ingred_create_1 = [f'{ingredient}/용량' for ingredient in ingred_create_list]
        ingred_create = ', '.join(ingred_create_1)
        cate_create = json.loads(flask_response.text, encoding="UTF-8").get('cate_create')
        
        cate_create_1 = cate_create[0]
        cate_create_2 = cate_create[1]
        cate_create_3 = cate_create[2]
 
            
        context = {
            'image_file': image_file,
            'ingred_create': ingred_create,
            'cate_create': cate_create,
            'cate_create_1': cate_create_1,
            'cate_create_2': cate_create_2,
            'cate_create_3': cate_create_3,
        }
        return render(request, 'post_form.html', context)

def get_latest_file(directory_path):
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    if not files:
        return None  # 디렉토리에 파일이 없는 경우
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
    
    
    return latest_file

def copy_latest_file_and_get_name(source_directory, destination_directory):
    # 최신 파일 가져오기
    latest_file = get_latest_file(source_directory)

    if latest_file:
        source_path = os.path.join(source_directory, latest_file)
        destination_path = os.path.join(destination_directory, latest_file)

        # 파일 복사
        shutil.copy2(source_path, destination_path)
        print(f"File '{latest_file}' copied from {source_directory} to {destination_directory}")

        # 복사된 파일 이름 반환
        return latest_file
    else:
        print(f"No files found in {source_directory}")
        return None

@login_required
def create(request):
    if request.method == 'POST':
        
        post = Post()
        print(request.POST)
        post.user = request.user
        post.title = request.POST['title']
        
        post.image = f'/image/post/{copy_latest_file_and_get_name("/home/ubuntu/web/cnn_flask/uploads", "/home/ubuntu/web/recipe_web/media/image/post")}'
        post.serving = int(request.POST['serving'])
        
        post.cate1 = request.POST['cate1']
        post.cate2 = request.POST['cate2']
        post.cate3 = request.POST['cate3']
    
        post.save()
        
        ingreddetails = request.POST.get('ingred').split(",")
        recipedetails = request.POST.get('recipe').split(",")

        for ingreddetail in ingreddetails:
            recipeingred = RecipeIngred()
            if ingreddetail:
                if not ingreddetail:
                    continue
                ingred = ingreddetail.split('/')[0]
                amount = ingreddetail.split('/')[1]
                _ingred, created = Ingred.objects.get_or_create(ingred_name=ingred)
                
                recipeingred.post = post
                recipeingred.ingred = _ingred
                recipeingred.amount = amount

                recipeingred.save()

                
        for recipe in recipedetails:
            recipedetail = RecipeDetail()
            if recipe:
                if not recipe:
                    continue
                step = recipe.split('/')[0]
                recipecontent = recipe.split('/')[1]
                
                recipedetail.post = post
                recipedetail.step = step
                recipedetail.contents = recipecontent

                recipedetail.save()
        post_id = post.id
        return redirect("posts:post_detail", post_id=post_id)
    
    else:
        form = PostForm()
    return render(request, 'temp_create_by_img.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    ingreds = RecipeIngred.objects.filter(post_id = post_id)
    recipes = RecipeDetail.objects.filter(post_id = post_id)
    rating_sum = (Rating.objects.filter(post_id = post_id).aggregate(Sum('score')))['score__sum']
    rating_num = Rating.objects.filter(post_id = post_id).count()
    if rating_num:
        rating_avg = round(rating_sum/rating_num,1)
    else:
        rating_avg = 0

    post.update_counter ## 조회수 늘리는 함수
    context = {
        'post': post,
        'ingreds': ingreds,
        'recipes': recipes,
        'rating_avg': rating_avg,
    }
    logger.info('', extra={'userid': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'postid': post.id, 'posttitle': post.title, 'postcate1': post.cate1, 'postcate2': post.cate2, 'postcate3': post.cate3, 'ip': get_client_ip(request) , 'modulename': 'detail'})
    return render(request, 'post_detail.html', context)


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
        return redirect('posts:index')

@login_required
def bookmark(request, post_id):

    # 즐겨찾기 버튼을 누른 유저
    user = request.user
    post = Post.objects.get(id=post_id)

    # 이미 즐겨찾기 버튼을 누른경우
    if post in user.bookmark_posts.all():
        post.bookmark_users.remove(user)
    # 즐겨찾기 버튼을 아직 안누른경우
    else:
        post.bookmark_users.add(user)
        logger.info('', extra={'userid': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'postid': post.id, 'posttitle': post.title, 'postcate1': post.cate1, 'postcate2': post.cate2, 'postcate3': post.cate3, 'ip': get_client_ip(request), 'modulename': 'bookmark' })
    return redirect("posts:post_detail", post_id=post_id)



# 종류별 네브바
def index_cate1_1(request):
    posts = Post.objects.filter(cate1='한식').order_by('-id')
    context = {
        'posts': posts,
        'index': '종류별>한식'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '한식', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate1_2(request):
    posts = Post.objects.filter(cate1='양식').order_by('-id')
    context = {
        'posts': posts,
        'index': '종류별>양식'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '양식', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate1_3(request):
    posts = Post.objects.filter(cate1='일식').order_by('-id')
    context = {
        'posts': posts,
        'index': '종류별>일식'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '일식', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate1_4(request):
    posts = Post.objects.filter(cate1='기타').order_by('-id')
    context = {
        'posts': posts,
        'index': '종류별>기타'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '일식', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)

# 상황별
def index_cate2_1(request):
    posts = Post.objects.filter(cate2='모임용').order_by('-id')
    context = {
        'posts': posts,
        'index': '상황별>모임용'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '모임용', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate2_2(request):
    posts = Post.objects.filter(cate2='원팬/스피디').order_by('-id')
    context = {
        'posts': posts,
        'index': '상황별>원팬/스피디'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '원팬/스피디', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate2_3(request):
    posts = Post.objects.filter(cate2='술안주').order_by('-id')
    context = {
        'posts': posts,
        'index': '상황별>술안주'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '술안주', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate2_4(request):
    posts = Post.objects.filter(cate2='일상').order_by('-id')
    context = {
        'posts': posts,
        'index': '상황별>일상'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '일상', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate2_5(request):
    posts = Post.objects.filter(cate2='다이어트').order_by('-id')
    context = {
        'posts': posts,
        'index': '상황별>다이어트'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '다이어트', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate2_6(request):
    posts = Post.objects.filter(cate2='디저트').order_by('-id')
    context = {
        'posts': posts,
        'index': '상황별>디저트'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '디저트', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)


# 재료별
def index_cate3_1(request):
    posts = Post.objects.filter(cate3='소고기').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>소고기'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '소고기', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_2(request):
    posts = Post.objects.filter(cate3='돼지고기').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>돼지고기'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '돼지고기', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_3(request):
    posts = Post.objects.filter(cate3='닭고기').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>닭고기'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '닭고기', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_4(request):
    posts = Post.objects.filter(cate3='육류').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>육류'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '육류', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_5(request):
    posts = Post.objects.filter(cate3='채소').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>채소'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '채소', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_6(request):
    posts = Post.objects.filter(cate3='생선').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>생선'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '생선', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_7(request):
    posts = Post.objects.filter(cate3='해물').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>해물'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '해물', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_8(request):
    posts = Post.objects.filter(cate3='쌀').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>쌀'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '쌀', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_9(request):
    posts = Post.objects.filter(cate3='밀가루').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>밀가루'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '밀가루', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_10(request):
    posts = Post.objects.filter(cate3='콩/견과류').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>콩/견과류'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '콩/견과류', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_11(request):
    posts = Post.objects.filter(cate3='달걀/유제품').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>달걀/유제품'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '달걀/유제품', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_12(request):
    posts = Post.objects.filter(cate3='가공식품류').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>가공식품류'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '가공식품류', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_13(request):
    posts = Post.objects.filter(cate3='기타').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>기타'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '기타', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
def index_cate3_14(request):
    posts = Post.objects.filter(cate3='면').order_by('-id')
    context = {
        'posts': posts,
        'index': '재료별>면'}
    logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'selectcate_name': '면', 'ip': get_client_ip(request), 'modulename': 'cateselect'})
    return render(request, 'index_cate.html', context)
        
        


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']      
        posts = Post.objects.filter(
            Q(title__icontains=searched) | Q(cate1__icontains=searched)|
            Q(cate2__icontains=searched) | Q(cate3__icontains=searched))
        context = {
            'searched': searched, 
            'posts': posts,  
        }
        logger.info('', extra={'user': request.user.username, 'sex': request.user.sex, 'age': request.user.age, 'searchword': searched, 'ip': get_client_ip(request),'modulename': 'search' })
        return render(request, 'searched.html', context)
    else:
        return render(request, 'searched.html', {})




def recommend(request):
    
    if request.POST:
        list_item = request.POST.getlist('selected')

        recommend_list = recommend_recipe(list_item)

        posts = Post.objects.filter(id__in=recommend_list[:16])
        context = {
            'posts': posts,
        }

        return render(request, 'recommend_list.html', context)
    else:
        return render(request, 'recommend.html')
    
@login_required
def rating_create(request, post_id):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = Rating()
            rating.user = request.user
            rating.post = Post.objects.get(id=post_id)
            rating.score = form.cleaned_data['score']
            rating.save()
            
            return redirect("posts:post_detail", post_id=post_id)
    else:
        form = RatingForm()
    return render(request, 'rating_form.html', {'form': form})

    

def imgsearch(request):
    if request.method == 'POST':
        image_file = request.FILES['search_image']
        files = {'image': (image_file.name, image_file.read())}
        
        flask_response = requests.post('보안상삭제', files=files)
    
        img_search_result = json.loads(flask_response.text, encoding="UTF-8").get('result')
        
        posts = []
        for result in img_search_result:
            post = Post.objects.filter(title__icontains=result).order_by('post_hit')[:5]
            posts.extend(post)
            
        context = {
            'image': '이미지검색',
            'posts': posts
        }
        return render(request, 'searched.html', context)
    