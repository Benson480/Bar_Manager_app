from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .models import UserSetting
from django.contrib.auth.models import AnonymousUser  # Import AnonymousUser

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

def user_settings(request):
    # Check if the user is authenticated before accessing settings
    if request.user.is_authenticated:
        user_settings, created = UserSetting.objects.get_or_create(user=request.user)
    else:
        # If the user is not authenticated, provide default settings or handle as needed
        user_settings = UserSetting()  # You can set default values here

    return {
        'user_settings': user_settings,
    }