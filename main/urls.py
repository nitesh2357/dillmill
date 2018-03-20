from django.conf.urls import url
from main.views import *

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^profile/$', Profile.as_view(), name='profile'),
    url(r'^update_profile/$', UpdateProfile.as_view(), name='update_profile'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^swipe/$', Swipe.as_view(), name='swipe'),
    url(r'^matched_list/$', MatchedList.as_view(), name='matched_list'),
]
