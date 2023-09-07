from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps


def login_required(redirect_to='/login/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                if redirect_to is None:
                    return redirect('login')  # Redirect to the login page by default
                else:
                    return redirect(reverse(redirect_to))
        return _wrapped_view
    return decorator

def public_view(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect authenticated users away from this view
            return redirect(reverse('dashboard'))  # Change 'dashboard' to the desired URL
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def login_exempt(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Check if the request URL matches any of the exempt URLs
        exempt_urls = ['about/', 'anouncement/', 'contacts/']
        if request.path_info in exempt_urls:
            return view_func(request, *args, **kwargs)
        elif not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapped_view