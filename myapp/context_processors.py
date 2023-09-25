from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

def include_login_form(request):
    form = AuthenticationForm()
    return {'form': form}

def user_profile(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            # Create a UserProfile instance if it doesn't exist
            user_profile = UserProfile.objects.create(user=request.user)
    return {'user_profile': user_profile}