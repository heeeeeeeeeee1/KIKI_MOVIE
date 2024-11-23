# accounts/urls.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    perform_create = staticmethod(lambda serializer: serializer.save())

    create = staticmethod(lambda self, request, *args, **kwargs: (
        self.get_serializer(data=request.data).is_valid(raise_exception=True),
        self.perform_create(self.get_serializer(data=request.data)),
        Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
    )[2])
