# middleware.py

import datetime
from django.conf import settings
from django.contrib.auth import logout

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')
            auto_logout_time = getattr(settings, 'AUTO_LOGOUT_TIME', 300)  # Default to 5 minutes

            if last_activity_str is not None:
                last_activity = datetime.datetime.fromisoformat(last_activity_str)  # Convert to datetime
                idle_duration = datetime.datetime.now() - last_activity
                if idle_duration.seconds >= auto_logout_time:
                    logout(request)
                    if 'last_activity' in request.session:  # Check if the key exists before deletion
                        del request.session['last_activity']

            # Update or set the 'last_activity' key in the session
            request.session['last_activity'] = datetime.datetime.now().isoformat()

        response = self.get_response(request)
        return response
