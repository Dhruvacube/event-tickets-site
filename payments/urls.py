from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('make_order/', make_order, name='make_order'),
    path('create_payment/', create_payment, name='create_payment'),
    url(r'^payment_stats', payment_stats, name='payment_stats'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)