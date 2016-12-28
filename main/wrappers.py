from django.http import HttpResponseForbidden

def check_access_right(users):
    def wrapper(fn):
        def wrapper_wrapper(request):
            if request.user.scholluser.role in users:
                return fn(request)
            else:
                return HttpResponseForbidden()
        return wrapper_wrapper
    return wrapper
