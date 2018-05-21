"""app urls"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from config import local
from . import views

urlpatterns = [
    url(r'^$', views.QuestionsList.as_view(), name='questions_list'),
    url(r'^list/$', views.QuestList, name='quest_list'),
    url(r'^(?P<pk>\d+)/$', views.AnswerView.as_view(), name='detail'),
    url(r'^question_create/$', views.QuestionCreate.as_view(), name='question_create'),
    url(r'^user_create/$', views.user_create, name='user_create'),
    url(r'^user/(?P<pk>\d+)/$', views.user_setting, name='user_setting'),
    url(r'^question/(?P<pk>\d+)/$', views.q_and_a, name='q_and_a'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^log_out/$', views.log_out, name='log_out'),    
]

if local.DEBUG:
    import debug_toolbar
    urlpatterns += staticfiles_urlpatterns() + static(local.MEDIA_URL, document_root=local.MEDIA_ROOT)
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)),] + urlpatterns
