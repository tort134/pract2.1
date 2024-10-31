from django.urls import path, include
from .views import user_login, user_logout, register, profile, create_request, delete_request
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = ([
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('create-request/', create_request, name='create_request'),
    path('delete_request/<int:request_id>/', delete_request, name='delete_request'),
]
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
