from django.conf.urls import url

from .views import ( ProfileRetrieveView, ProfileUpdateView )

urlpatterns = [
    url(r'^userprofile/$', ProfileRetrieveView.as_view()),
    url(r'^updateprofile/$', ProfileUpdateView.as_view()),
]
