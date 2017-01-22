from django.http import HttpResponseForbidden
from models import SchollUser

def check_access_right(users):
    def wrapper(fn):
        def wrapper_wrapper(request, id=None):
            if not hasattr(request.user, 'scholluser') or not getattr(request.user, 'scholluser'):
                scholluser = SchollUser.objects.filter(user_ptr_id = request.user.id)
                scholluser = scholluser[0] if scholluser else None
            else:
                scholluser = request.user.scholluser

            if scholluser and scholluser.role in users or request.user.is_staff or request.is_ajax():
                return fn(request, id)
            else:
                return HttpResponseForbidden()
        return wrapper_wrapper
    return wrapper
