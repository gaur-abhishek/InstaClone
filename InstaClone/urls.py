from django.conf.urls import url

from myapp.views import signup_view, feed_view, login_view, post_view, like_view, comment_view, logout_view, upvoting_view, search_view
urlpatterns = [
    url('post/', post_view),
    url('feed/', feed_view),
    url('like/', like_view),
    url('comment/', comment_view),
    url('login/', login_view),
    url('', signup_view),
    url('logout/', logout_view),
    url('upvoting/', upvoting_view),
    url('search/', search_view)
]