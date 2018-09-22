from django.shortcuts import redirect

profile_page = '/accounts/info/'
allowed = [profile_page]

def EnsureMiddleware(get_response):
    def middleware(request):
        if request.user.is_superuser \
            or request.user.is_anonymous \
            or request.user.is_staff:
            return get_response(request)

        if request.path in allowed:
            return get_response(request)

        if request.user.profile_set.first() == None:
            return redirect(profile_page)

        return get_response(request)

    return middleware