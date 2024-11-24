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
    user = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)  # 댓글 배열을 포함
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    # CONFLICT > user = serializers.CharField(source='user.username', read_only=True)  # 사용자 이름만 포함
    # CONFLICT > comments = CommentSerializer(many=True, read_only=True)  # 연결된 댓글 포함

    class Meta:
        model = Review
        fields = [
            'id', 'content', 'score', 'created_at', 'user', 
            'comments', 'comment_count', 'like_count'
        ]

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_like_count(self, obj):
        return obj.likes.count()

# -------------------------------------------------------

# 전체 영화 조회
class AllMovieSerializer(serializers.ModelSerializer):
    genres = GenreListSerializer(many=True, read_only=True)
    actors = ActorListSerializer(many=True, read_only=True)
    directors = DirectorListSerializer(many=True, read_only=True)
    keywords = KeywordListSerializer(many=True, read_only=True)
    videos = VideoListSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    is_in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
    
    def get_is_in_wishlist(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(movie=obj, user=request.user).exists()
        return False
# - 영화 가져올 때 해당 영화 리뷰?
# - 리뷰 가져올 때 해당 댓글도 같이?
        

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