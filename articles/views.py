from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core import mongoops

from datetime import datetime
# Create your views here.


class ArticlePostView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        username = request.user.email
        article_data = request.data

        id = mongoops.numDocuments('articles') + 1
        article_data['article']['article_id'] = id
        article_data['article']['created_at'] = datetime.now()
        article_data['article']['updated_at'] = datetime.now()
        article_data['user'] = {'username': username}
        mongoops.insertDocument('articles', article_data)

        filter = {
            'article.article_id': id
        }
        response = mongoops.getDocument('articles', filter)

        return Response(response, status=status.HTTP_201_CREATED)


class ArticleGetView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        username = request.user.email
        query_params = self.request.query_params

        if len(query_params) == 0:
            filter = None
        else:
            filter = {
                'article.article_id':  int(query_params['id'])
            }

        response = mongoops.getDocuments('articles', filter)

        return Response(response, status=status.HTTP_200_OK)
