from django.http import HttpResponse
from django.shortcuts import redirect, render

def unaunthenticated_user(view_func):
    def wrapper_func(req, *args, **kwargs):
        if req.user.is_authenticated:
            return redirect('signin')
        else:
            return view_func(req, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(req, *args, **kwargs):
            print('working:', allowed_roles)
            group=None
            if req.user.groups.exists():
                group=req.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(req, *args, **kwargs)
            else:
                return render(req, '404.html')
        return wrapper_func
    return decorator
