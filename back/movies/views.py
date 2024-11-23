# movies/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# ---------- 영화 ----------
# 전체 영화 조회(메인페이지)
@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = AllMovieSerializer(movies, many=True)
    return Response(serializer.data)


################################# MovieDetailView ######################################
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    # 로그인 여부 확인
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, movie=movie).exists()

    serializer = MovieSerializer(movie, context={'request': request})
    movie_data = serializer.data
    movie_data['is_in_wishlist'] = is_in_wishlist  # 보고싶어요 상태 추가

    return Response(movie_data, status=status.HTTP_200_OK)

""" CONFLICT >
# 영화 단일 조회(상세정보)
@api_view(['GET'])
def movie_detail(request, movie_pk):
    # prefetch_related로 ManyToManyField 데이터를 미리 로드
    movie = get_object_or_404(Movie.objects.prefetch_related('genres', 'actors', 'directors', 'keywords', 'videos'), pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
"""

# 영화에 연결된 리뷰 리스트를 반환하는 API
@api_view(['GET'])
def movie_reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, movie_pk):
    movie = Movie.objects.filter(pk=movie_pk).first()
    if not movie:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_wishlist(request, movie_pk):
    user = request.user
    movie = Movie.objects.filter(pk=movie_pk).first()

    if not movie:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    wishlist_item = Wishlist.objects.filter(user=user, movie=movie).first()

    if wishlist_item:
        wishlist_item.delete()
        return Response({"message": "Wishlist removed"}, status=status.HTTP_200_OK)
    else:
        Wishlist.objects.create(user=user, movie=movie)
        return Response({"message": "Added to wishlist"}, status=status.HTTP_201_CREATED)

################################# ReviewDetailView ######################################
# 특정 영화의 특정 리뷰 조회
@api_view(['GET'])
def movie_review(request, movie_pk, review_pk):
    # 영화와 리뷰가 존재하는지 확인
    review = get_object_or_404(Review, pk=review_pk, movie_id=movie_pk)

# ---------- 리뷰 ----------
# 리뷰 조회, 생성, 수정, 삭제
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def review_handler(request, movie_pk, review_pk):
    # 리뷰 조회 (GET - 전체 리뷰 또는 단일 리뷰)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

# 리뷰 좋아요 추가 제거
@api_view(['POST'])
def like_review(request, review_pk):
    try:
        review = Review.objects.get(pk=review_pk)
        review.like_count += 1  # 좋아요 수 증가
        review.save()
        return Response({'like_count': review.like_count}, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def toggle_like_review(request, review_pk):
    try:
        review = Review.objects.get(pk=review_pk)
        user = request.user
        # 이미 좋아요를 눌렀는지 확인
        existing_like = ReviewLike.objects.filter(review=review, user=user).first()
        liked = False
        if existing_like:
            # 좋아요 취소
            existing_like.delete()
        else:
            # 좋아요 추가
            ReviewLike.objects.create(review=review, user=user)
            liked = True
        return Response({'liked': liked, 'like_count': review.likes.count()}, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
"""CONFLICT > 
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
"""
