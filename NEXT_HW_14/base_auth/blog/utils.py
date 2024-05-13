import datetime
from functools import wraps
import re
import unicodedata
from pytz import timezone
from django.shortcuts import get_object_or_404, render
from .models import Post


def is_owner_or_admin(request, obj):
    return obj.creator == request.user or request.user.is_superuser


def update_post_lasted_viewed():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 선택한 인자를 kwrags에서 가져옵니다. kwargs는 URL 매칭에서 전달된 인자를 포함합니다.
            post_pk = kwargs.get("post_pk")
            if not post_pk:
                return render(request, "error.html", {"error": "post_pk not found."})

            # Retrieve the object based on ID and your model
            # You might need to adjust this part based on how your models are structured
            post = get_object_or_404(Post, **{"pk": post_pk})

            post.last_viewed_user = request.user
            post.last_viewed_datetime = datetime.datetime.now(timezone("Asia/Seoul"))
            post.save()

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def get_new_file_name(file, user, title):
    file_extension = file.name.split(".")[-1]
    cleaned_title = clean_title(title)
    new_file_name = (
        cleaned_title
        if cleaned_title
        else datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    )
    new_file_name = f"blog/{user.username}/{new_file_name}.{file_extension}"
    return new_file_name


def clean_title(title):
    """
    Clean and sanitize the title by removing or replacing special characters.
    """
    title = (
        unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    )  # Normalize and remove non-ascii chars
    title = re.sub(
        r"[^\w\s-]", "", title
    ).strip()  # Remove special characters except for underscores, hyphens, and whitespace
    title = re.sub(
        r"[-\s]+", "-", title
    )  # Replace whitespace or sequence of dashes with a single dash
    return title
