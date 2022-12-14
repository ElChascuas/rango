from django.contrib import admin
from django.urls import path, include
from si.view import index, about_us
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", index, name="index.html"),
    path("about-us/", about_us, name="about_us.html"),
    path("admin/", admin.site.urls),
    path("products/", include("products.urls")),
    path("blog/", include("blog.urls")),
    path("characters/", include("characters.urls")),
    path("users/", include("users.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
