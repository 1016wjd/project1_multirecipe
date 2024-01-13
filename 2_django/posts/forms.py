from django import forms
from .models import Post, Rating

class PostForm(forms.Form):
    title = forms.CharField(max_length=128, label='제목',
      error_messages={
        'required': '제목을 입력해 주세요'
      })
    
    image = forms.ImageField()
    
    serving = forms.IntegerField(label='인분',
    error_messages={
        'required': '제목을 입력해 주세요'
      })
    
    ingredsdetails = forms.CharField(label='재료',
      error_messages={
        'required': '내용을 입력해 주세요'
      })

    recipedetails = forms.CharField(label='레시피',
      widget=forms.TextInput(
          attrs={"class": "recipe-input"}
      ),
      
      error_messages={
        'required': '내용을 입력해 주세요'
      })
    
    CATE_CHOICES1 = (('한식', '한식'), ('양식', '양식'), ('일식', '일식'), ('기타', '기타'))
    cate1 = forms.ChoiceField(
        choices = CATE_CHOICES1,
        widget = forms.Select()
    )

    CATE_CHOICES2 = (('모임용', '모임용'), ('원팬/스피디', '원팬/스피디'), ('술안주', '술안주'), ('일상', '일상'), ('다이어트', '다이어트'), ('디저트', '디저트')) 
    cate2 = forms.ChoiceField(
        choices = CATE_CHOICES2,
        widget = forms.Select()
    )
    CATE_CHOICES3 = (('소고기' ,'소고기'),('돼지고기' ,'돼지고기'),('닭고기' ,'닭고기'),('육류' ,'육류'),('채소' ,'채소'),('생선' ,'생선'),('해물' ,'해물'),('쌀' ,'쌀'),('밀가루' ,'밀가루'),('면' ,'면'),('콩/견과류' ,'콩/견과류'),('달걀/유제품' ,'달걀/유제품'),('가공식품류' ,'가공식품류'),('기타' ,'기타'))
    cate3 = forms.ChoiceField(
        choices = CATE_CHOICES3,
        widget = forms.Select()
    )
    
class RatingForm(forms.Form):
    SCORE_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    score = forms.ChoiceField(
        choices = SCORE_CHOICES,
        widget = forms.Select()
    )