from django.conf.urls import url

from .views import ( ProfileRetrieveView, ProfileUpdateView )

urlpatterns = [
    url(r'^get/$', ProfileRetrieveView.as_view()),
    url(r'^update/$', ProfileUpdateView.as_view()),
]
