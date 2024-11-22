from rest_framework import serializers
from .models import *

# 영화 정보(장르, 배우, 감독, 키워드, 비디오)
class GenreListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Genre
        fields = '__all__'


class ActorListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Actor
        fields = '__all__'


class DirectorListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Director
        fields = '__all__'


class KeywordListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Keyword
        fields = '__all__'


class VideoListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Video
        fields = '__all__'

# --------------------------------------------------

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)  # 사용자 이름만 포함

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user']


# 리뷰
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)  # 사용자 이름만 포함
    comments = CommentSerializer(many=True, read_only=True)  # 연결된 댓글 포함

    class Meta:
        model = Review
        fields = ['id', 'content', 'score', 'created_at', 'user', 'comments']

# -------------------------------------------------------

# 전체 영화 조회
class AllMovieSerializer(serializers.ModelSerializer):
    genres = GenreListSerializer(many=True, read_only=True)
    actors = ActorListSerializer(many=True, read_only=True)
    directors = DirectorListSerializer(many=True, read_only=True)
    keywords = KeywordListSerializer(many=True, read_only=True)
    videos = VideoListSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)  # 연결된 리뷰 포함

    class Meta:
        model = Movie
        fields = '__all__'
        

# 단일 영화 항목 조회
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreListSerializer(many=True, read_only=True)
    actors = ActorListSerializer(many=True, read_only=True)
    directors = DirectorListSerializer(many=True, read_only=True)
    keywords = KeywordListSerializer(many=True, read_only=True)
    videos = VideoListSerializer(many=True, read_only=True)
    
    # 해당 영화의 리뷰도 함께 가져오기
    class ReviewListSerializer(serializers.ModelSerializer):
        class CommentListSerializer(serializers.ModelSerializer):
            user = serializers.CharField(source='user.username', read_only=True)  # 사용자 이름만 포함
        
            class Meta:
                model = Comment
                fields = '__all__'
        
        comment_set = CommentListSerializer(many=True, read_only=True)
        user = serializers.CharField(source='user.username', read_only=True)  # 사용자 이름만 포함
        
        class Meta:
            model = Review
            fields = '__all__'
            
    review_set = ReviewListSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'