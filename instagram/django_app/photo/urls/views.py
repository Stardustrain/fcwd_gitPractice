from django.conf.urls import url
from .. import views

urlpatterns = [
    # url(r'^photo/$', views.photo_list, name='photo_list'),
    url(r'^photo_list/$', views.PhotoList.as_view(), name='photo_list'),
    url(r'^photo_add/$', views.PhotoAdd.as_view(), name='photo_add'),
    url(r'^photo_detail/(?P<pk>\d+)/$', views.PhotoDetail.as_view(), name='photo_detail'),
    url(r'^photo/delete/$', views.photo_delete, name='photo_delete'),
]
