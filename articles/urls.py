from django.conf.urls import url
from .views import ( ArticlePostView, ArticleGetView )

urlpatterns = [
    url('^insert/$', ArticlePostView.as_view()),
    url('^get/$', ArticleGetView.as_view()),
]
