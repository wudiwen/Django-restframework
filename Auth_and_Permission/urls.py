from django.conf.urls import url

from Auth_and_Permission import views

urlpatterns = [
    url(r'^users/', views.UserAPI.as_view()),
    url(r'^blogs/', views.BlogsAPIView.as_view()),

]