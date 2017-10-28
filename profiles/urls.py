from django.conf.urls import url

from .views import ( ProfileRetrieveView )

urlpatterns = [
    url(r'^userprofile/$', ProfileRetrieveView.as_view()),
]
