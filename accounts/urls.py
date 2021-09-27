from django.conf.urls import url
from django.urls import path,re_path
from .views import PasswordResetViews, PasswordResetDoneViews, PasswordResetConfirmViews
from django.contrib.auth.views import PasswordResetCompleteView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("password_reset/", PasswordResetViews.as_view(),name='password_reset'),
    url('password_reset/done/', PasswordResetDoneViews.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmViews.as_view(), name='password_reset_confirm'),
    re_path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^changepassword/$', views.change_password, name='change_password'),
    
    url(r'^login/$', views.loginform, name='signin'),
    url(r'^logout/$', views.user_logout, name='signout'),
    path('signup/', views.signup, name='signup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)