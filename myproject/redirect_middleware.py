from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define a list of URLs that can be accessed without authentication
        allowed_urls = [
            reverse('login'),
            reverse('index'),
            reverse('about'),
            reverse('announcements'),
            reverse('contacts'),
            reverse('admin:index'),  # Use 'admin:index' for the Django admin dashboard
            reverse('add_to_cart', kwargs={'image_id': 0}),  # Include 'add_to_cart' with a placeholder image_id
            settings.MEDIA_URL,  # Allow access to MEDIA_URL
        ]

        # Check if the request path starts with the URLs in allowed_urls
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in allowed_urls):
            return redirect('index')  # Redirect to 'index' for unauthenticated users

        response = self.get_response(request)
        return response
