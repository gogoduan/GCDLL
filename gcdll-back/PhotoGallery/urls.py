from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views import static

urlpatterns = [
    # 利用include()函数为board应用添加前缀为api的路由
    # ----------------------------------------------
    path("admin/", admin.site.urls),
    path("api/", include("gallery.urls")),
    path(
        r"^static/(?P<path>.*)$",
        static.serve,
        {"document_root": settings.STATIC_ROOT},
        name="static",
    ),
]
