from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticated_user(view_func):
    def wraper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("classes")
        else:
            return view_func(request, *args, **kwargs)

    return wraper


def allowed_users(user_type):
    def view_wrap(view_func):
        def wraper(request, *args, **kwargs):
            if (
                request.user.is_authenticated
                and request.user.userclass.user_type == user_type
            ):
                return view_func(request, *args, **kwargs)
            else:
                return redirect("classes")

        return wraper

    return view_wrap
