from django.http import HttpResponseRedirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
