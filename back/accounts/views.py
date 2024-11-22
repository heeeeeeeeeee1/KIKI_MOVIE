# accounts/urls.py
from django.shortcuts import render

# Create your views here.
from .serializers import *
from movies.serializers import *

User = get_user_model()

# 개인 프로필 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserInfoSerializers(user)
    return Response(serializer.data)