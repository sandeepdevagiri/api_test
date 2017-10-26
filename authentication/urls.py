from django.conf.urls import url

from .views import ( RegistrationAPIView, LoginAPIView, AccountRetrieveUpdateAPIView )

urlpatterns = [
    url(r'^register/$', RegistrationAPIView.as_view()),
    url(r'^login/$', LoginAPIView.as_view()),
    url(r'^update/$', AccountRetrieveUpdateAPIView.as_view()),
]
