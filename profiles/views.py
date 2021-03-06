from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core import mongoops
# Create your views here.


class ProfileRetrieveView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        username = request.user.email
        filter = {
            'user.username': username
        }
        response = mongoops.getDocument('profile', filter)
        return Response(response, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        username = request.user.email
        profile_data = request.data
        filter = {
            'user.username': username
        }
        response = mongoops.updateDocument('profile', filter, profile_data)
        return Response(response, status=status.HTTP_200_OK)
