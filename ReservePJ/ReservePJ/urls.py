"""
Definition of urls for ReservePJ.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register.urls')),
]

# メールをコンソールに表示する
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'