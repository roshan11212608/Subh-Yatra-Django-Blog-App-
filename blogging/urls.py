
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header = "BLOGGING SYSTEM ADMIN PANEL"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to Blogging Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("home.urls")),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
