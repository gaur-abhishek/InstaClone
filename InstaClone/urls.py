from django.conf.urls import url

from myapp.views import signup_view
urlpatterns = [
    url('', signup_view)
]