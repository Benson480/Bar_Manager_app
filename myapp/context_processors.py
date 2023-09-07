from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

def include_login_form(request):
    form = AuthenticationForm()
    return {'form': form}
