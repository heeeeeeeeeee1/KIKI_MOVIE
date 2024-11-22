from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# 영화 리스트 조회(메인페이지)
@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


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
    review = get_object_or_404(Review, pk=review_pk, movie_id=movie_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


# 리뷰 저장 및 검증
@api_view(['POST'])
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(movie=movie, user=request.user)  # 사용자와 게시글 연결
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 저장 및 검증
@api_view(['POST'])
def comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
