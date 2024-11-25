# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import User
from movies.models import Review, Wishlist
from accounts.serializers import CustomUserDetailsSerializer
from movies.serializers import ReviewSerializer, MovieSerializer

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def custom_user_details(request):
    user = request.user

    if request.method == 'GET':
        # 사용자 기본 정보
        user_serializer = CustomUserDetailsSerializer(user)
        user_data = user_serializer.data
        # 사용자가 작성한 리뷰 (봤어요 목록)
        reviews = Review.objects.filter(user=user).select_related('movie')
        review_serializer = ReviewSerializer(reviews, many=True)
        # 사용자가 보고싶어요한 영화
        wishlist = Wishlist.objects.filter(user=user).select_related('movie')
        wishlist_movies = [wishlist_item.movie for wishlist_item in wishlist]
        wishlist_serializer = MovieSerializer(wishlist_movies, many=True)
        # 데이터 통합 반환
        data = {
            'user_info': user_data,
            'watched_reviews': review_serializer.data,
            'wishlist': wishlist_serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)

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
