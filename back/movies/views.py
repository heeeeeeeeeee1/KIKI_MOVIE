from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import *
from .serializers import *

# 영화 리스트 조회 및 생성
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def movie_list(request):    # 메인페이지에서 쓰겠지
#     # GET 요청: 영화 리스트 반환
#     if request.method == 'GET':
#         movies = get_list_or_404(Movie)
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     # POST 요청: 영화 생성하진 않을텐데
#     elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# 영화 상세 정보 조회
@api_view(['GET'])
def movie_detail(request, movie_pk):
    # prefetch_related로 ManyToManyField 데이터를 미리 로드
    movie = get_object_or_404(Movie.objects.prefetch_related('genres', 'actors', 'directors', 'keywords', 'videos'), pk=movie_pk)

    serializer = MovieSerializer(movie)
    return Response(serializer.data)

# 특정 영화의 특정 리뷰 조회
@api_view(['GET'])
def movie_review(request, movie_pk, review_pk):
    # 영화와 리뷰가 존재하는지 확인
    review = get_object_or_404(Review, pk=review_pk, movie_id=movie_pk)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
