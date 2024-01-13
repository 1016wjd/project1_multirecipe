from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # model = get_user_model()
        model = User
        fields = ('username', 'sex', 'age')
        
        
class CustomAuthenticationForm(AuthenticationForm):
    pass