# accounts/urls.py
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import CustomUserDetailsSerializer

@api_view(['GET'])
def custom_user_details(request):
    user = request.user  # 현재 로그인한 사용자
    serializer = CustomUserDetailsSerializer(user)
    print(user)
    return Response(serializer.data)
# class SignUpView(generics.CreateAPIView):
#     serializer_class = UserSerializer

#     perform_create = staticmethod(lambda serializer: serializer.save())

#     create = staticmethod(lambda self, request, *args, **kwargs: (
#         self.get_serializer(data=request.data).is_valid(raise_exception=True),
#         self.perform_create(self.get_serializer(data=request.data)),
#         Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
#     )[2])
