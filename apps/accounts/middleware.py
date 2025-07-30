from django.utils.timezone import now

class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session = request.session
        today = now().date().isoformat()

        # Use a session key to track if today has already been counted
        if not session.get(f'visited_today_{today}', False):
            visits = session.get('visit_history', {})
            visits[today] = visits.get(today, 0) + 1
            session['visit_history'] = visits

            # Mark that today's visit has been counted for this session
            session[f'visited_today_{today}'] = True

        # Always update last_visit for personalization
        session['last_visit'] = now().strftime('%B %d, %Y at %I:%M %p')

        return self.get_response(request)
