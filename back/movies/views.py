# movies/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# ---------- 영화 ----------
# 전체 영화 조회(메인페이지)
@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = AllMovieSerializer(movies, many=True)
    return Response(serializer.data)


# 영화 단일 조회(상세정보)
@api_view(['GET'])
def movie_detail(request, movie_pk):
    # prefetch_related로 ManyToManyField 데이터를 미리 로드
    movie = get_object_or_404(Movie.objects.prefetch_related('genres', 'actors', 'directors', 'keywords', 'videos'), pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# ---------- 리뷰 ----------
# 리뷰 조회, 생성, 수정, 삭제
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def review_handler(request, movie_pk, review_pk):
    # 리뷰 조회 (GET - 전체 리뷰 또는 단일 리뷰)
    if request.method == 'GET':
        if review_pk:  # 단일 리뷰 조회
            review = get_object_or_404(Review, pk=review_pk, movie_id=movie_pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:          # 전체 리뷰 조회
            reviews = get_list_or_404(Review, movie_id=movie_pk)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)

    # 리뷰 생성 (POST - 로그인 필요)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 리뷰 수정 (PUT - 로그인 필요)
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        review = get_object_or_404(Review, pk=review_pk, movie_id=movie_pk, user=request.user)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 리뷰 삭제 (DELETE - 로그인 필요)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        review = get_object_or_404(Review, pk=review_pk, movie_id=movie_pk, user=request.user)
        review.delete()
        return Response({'detail': '삭제 완료'}, status=status.HTTP_204_NO_CONTENT)


# ---------- 댓글 ----------
# 댓글 조회, 생성, 수정, 삭제
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def comment_handler(request, movie_pk, review_pk, comment_pk):
    # 댓글 조회 (GET - 전체 댓글 또는 단일 댓글)
    if request.method == 'GET':
        if comment_pk:  # 단일 댓글 조회
            comment = get_object_or_404(Comment, pk=comment_pk, review_id=review_pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:  # 전체 댓글 조회
            comments = get_list_or_404(Comment, review_id=review_pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    # 댓글 생성 (POST - 로그인 필요)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        review = get_object_or_404(Review, pk=review_pk, movie_id=movie_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(review=review, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 수정 (PUT - 로그인 필요)
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        comment = get_object_or_404(Comment, pk=comment_pk, review_id=review_pk, user=request.user)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 삭제 (DELETE - 로그인 필요)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        comment = get_object_or_404(Comment, pk=comment_pk, review_id=review_pk, user=request.user)
        comment.delete()
        return Response({'detail': '삭제 완료'}, status=status.HTTP_204_NO_CONTENT)
