# accounts/urls.py
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from rest_framework import status
from accounts.serializers import CustomUserDetailsSerializer

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def custom_user_details(request):
    user = request.user

    if request.method == 'GET':
        serializer = CustomUserDetailsSerializer(user)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        data = request.data.copy()
        data.pop('username', None)  # username 변경 요청 제거
        serializer = CustomUserDetailsSerializer(user, data=data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SignUpView(generics.CreateAPIView):
#     serializer_class = UserSerializer

#     perform_create = staticmethod(lambda serializer: serializer.save())

#     create = staticmethod(lambda self, request, *args, **kwargs: (
#         self.get_serializer(data=request.data).is_valid(raise_exception=True),
#         self.perform_create(self.get_serializer(data=request.data)),
#         Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
#     )[2])
