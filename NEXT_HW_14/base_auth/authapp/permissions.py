from functools import wraps
from django.shortcuts import get_object_or_404, render


def is_owner_or_admin(request, obj):
    return obj.creator == request.user or request.user.is_superuser

    
def check_is_creator_or_admin(model_cls, lookup_field="pk"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 선택한 인자를 kwrags에서 가져옵니다. kwargs는 URL 매칭에서 전달된 인자를 포함합니다.
            obj_id = kwargs.get(lookup_field)
            if not obj_id:
                return render(request, "error.html", {"error": "Object ID not found."})

            # Retrieve the object based on ID and your model
            # You might need to adjust this part based on how your models are structured
            obj = get_object_or_404(model_cls, **{"pk": obj_id})

            # Call the permission check function
            if not is_owner_or_admin(request, obj):
                return render(request, "error.html", {"error": "Permission denied."})

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
