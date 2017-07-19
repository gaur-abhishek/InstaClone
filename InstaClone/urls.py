from django.conf.urls import url

from myapp.views import signup_view, feed_view, login_view
urlpatterns = [
    url('feed/', feed_view),
    url('login/', login_view),
    url('', signup_view)
]