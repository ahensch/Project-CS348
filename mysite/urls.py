from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('', views.home, name='home'),        # ✅ new home route
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),        # keep this if you already have it
]
