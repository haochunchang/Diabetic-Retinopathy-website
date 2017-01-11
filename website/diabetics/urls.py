from django.conf.urls import url
from . import views


app_name = 'diabetics'
urlpatterns = [
    # ex: /diabetics/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /upload/
    url(r'^uploads/$', views.UploadsView.as_view(), name='uploads'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteView.as_view(), name='delete'),
    # ex: /diabetics/5/
    url(r'^(?P<imagename_id>[0-9]+)/$', views.individual, name='individual'),
    # ex: /diabetics/list_view/
    url(r'^list_view/$', views.ListView.as_view(), name='list_view'),
    # ex: /diabetics/summary/
    url(r'^summary/$', views.summary, name='summary'),

]
