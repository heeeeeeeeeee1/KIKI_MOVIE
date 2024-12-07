# movies/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import *
from .serializers import *

# MainHome #############################################################################
@api_view(['GET'])
def movie_list(request):
    """
    전체 영화 조회
    - /movies/에 연결됨
    """
    movies = get_list_or_404(Movie)
    serializer = AllMovieSerializer(movies, many=True)
    return Response(serializer.data)

# MovieDetailView ######################################################################
@api_view(['GET'])
def movie_detail(request, movie_pk):
    """
    단일 영화 정보 조회
    - /movies/<int:movie_pk>/detail/에 연결됨
    """
    movie = get_object_or_404(Movie, pk=movie_pk)
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, movie=movie).exists()
    serializer = MovieSerializer(movie, context={'request': request})
    movie_data = serializer.data
    movie_data['is_in_wishlist'] = is_in_wishlist  # 보고싶어요 상태 추가
    return Response(movie_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_wishlist(request, movie_pk):
    """
    단일 영화에 대한 보고싶어요 토글 버튼 클릭
    - /movies/<int:movie_pk>/wishlist/에 연결됨
    """
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

@api_view(['GET'])
def movie_reviews(request, movie_pk):
    """
    단일 영화에 연결된 리뷰 목록 조회
    - /movies/<int:movie_pk>/reviews/에 연결됨
    """
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, movie_pk):
    """
    영화에 대한 리뷰 생성
    - /movies/<int:movie_pk>/review/create/에 연결됨
    """
    movie = Movie.objects.filter(pk=movie_pk).first()
    if not movie:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ReviewDetailView ######################################################################

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    
    if request.method == 'GET':
        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data)
    
    # PUT과 DELETE는 인증 필요
    if not request.user.is_authenticated:
        return Response({'error': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    # 작성자만 수정/삭제 가능
    if request.user != review.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like_review(request, review_pk):
    """
    리뷰 좋아요 토글 기능
    """
    try:
        review = Review.objects.get(pk=review_pk)
        user = request.user
        # 좋아요가 이미 있는지 확인
        existing_like = ReviewLike.objects.filter(review=review, user=user).first()
        liked = False
        if existing_like:
            # 좋아요 취소
            existing_like.delete()
        else:
            # 좋아요 추가
            ReviewLike.objects.create(review=review, user=user)
            liked = True
        
        # 좋아요 수 반환
        return Response({
            'liked': liked,
            'like_count': review.likes.count()
        }, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.user != comment.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    """댓글 수정/삭제"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.user != comment.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def movie_tmdb(request, tmdb_id=None):
    if request.method == 'GET':
        movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
        if movie:
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        try:
            print("받은 데이터:", request.data)
            
            existing_movie = Movie.objects.filter(id=request.data.get('id')).first()
            if existing_movie:
                serializer = MovieSerializer(existing_movie)
                return Response(serializer.data)
            
            movie_data = request.data.copy()
            
            # 텍스트 필드에 대한 기본값 설정 (빈 문자열로)
            movie_data.setdefault('video_path', '')  # TextField는 빈 문자열로
            movie_data.setdefault('runtime', '0')
            movie_data.setdefault('status', 'Released')
            movie_data.setdefault('tagline', '')  # TextField는 빈 문자열로
            movie_data.setdefault('popularity', 0.0)
            movie_data.setdefault('adult', False)
            movie_data.setdefault('created_at', timezone.now().date().isoformat())
            
            # 필수 필드가 없는 경우 빈 값으로 설정
            if not movie_data.get('description'):
                movie_data['description'] = ''  # TextField는 빈 문자열로
            
            print("처리된 데이터:", movie_data)
            
            serializer = MovieSerializer(data=movie_data)
            if not serializer.is_valid():
                print("유효성 검사 오류:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            movie = serializer.save()
            
            # 장르 정보가 있다면 처리
            if 'genres' in request.data and request.data['genres']:
                for genre_name in request.data['genres']:
                    genre, _ = Genre.objects.get_or_create(name=genre_name)
                    movie.genres.add(genre)
            
            return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print("예외 발생:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_movie_actors(request, movie_pk):
    try:
        movie = Movie.objects.get(pk=movie_pk)
        actors_data = request.data.get('actors', [])
        for actor_data in actors_data:
            actor, created = Actor.objects.get_or_create(
                id=actor_data.get('id'),
                defaults={
                    'name': actor_data.get('name'),
                    'profile_path': actor_data.get('profile_path')
                }
            )
            movie.actors.add(actor)
        return Response(MovieSerializer(movie).data)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_movie_genres(request, movie_pk):
    try:
        movie = Movie.objects.get(pk=movie_pk)
        genres_data = request.data.get('genres', [])
        print("Received genres data:", genres_data)  # 디버깅용 출력
        
        for genre_data in genres_data:
            try:
                # genres가 문자열 배열로 올 경우
                if isinstance(genre_data, str):
                    genre, _ = Genre.objects.get_or_create(name=genre_data)
                # genres가 객체 배열로 올 경우
                else:
                    genre, _ = Genre.objects.get_or_create(
                        name=genre_data.get('name', '')
                    )
                movie.genres.add(genre)
                print(f"Added genre: {genre.name}")  # 디버깅용 출력
            except Exception as e:
                print(f"Error processing genre {genre_data}: {str(e)}")  # 디버깅용 출력
                continue

        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error in add_movie_genres: {str(e)}")  # 디버깅용 출력
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def add_movie_directors(request, movie_pk):
    try:
        movie = Movie.objects.get(pk=movie_pk)
        directors_data = request.data.get('directors', [])
        
        for director_data in directors_data:
            director, created = Director.objects.get_or_create(
                id=director_data.get('id'),
                defaults={
                    'name': director_data.get('name'),
                    'profile_path': director_data.get('profile_path')
                }
            )
            movie.directors.add(director)
            
        return Response(MovieSerializer(movie).data)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error adding directors: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# movies/views.py에 추가
@api_view(['GET'])
def all_reviews(request):
    """
    전체 리뷰 목록을 최신순으로 반환
    """
    reviews = Review.objects.select_related('movie', 'user').prefetch_related('comments', 'likes').order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_latest_review(request, username):
    """
    특정 사용자의 최신 리뷰 반환
    """
    try:
        latest_review = Review.objects.select_related('movie', 'user').filter(user__username=username).latest('created_at')
        serializer = ReviewSerializer(latest_review)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response({'message': 'No reviews found'}, status=status.HTTP_404_NOT_FOUND)