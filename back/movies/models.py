from django.db import models
from django.conf import settings
from django.utils.timezone import now

# 영화 정보 DB - 영화와 N:M 관계
class Actor(models.Model): # 배우 DB
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    profile_path = models.TextField(null=True, blank=True) # 프로필 이미지 주소
    # 이 부분 추가
    language = models.CharField(
    max_length=10,
    choices=[('ko-KR', 'Korean'), ('en-US', 'English')],
    default='en-US'
)


class Director(models.Model): # 감독 DB
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    profile_path = models.TextField(null=True, blank=True) # 프로필 이미지 주소


class Keyword(models.Model): # 키워드 DB
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Genre(models.Model): # 장르 DB
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Video(models.Model): # 비디오 DB
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    video_type = models.CharField(max_length=50)    # 사이트? 예) 유튜브
    site = models.CharField(max_length=50)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='videos')


class Movie(models.Model):  # 영화 DB
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=False, null=True, default=None)
    vote_average = models.FloatField()
    poster_path = models.TextField()
    video_path = models.TextField()
    popularity = models.FloatField()

    runtime = models.TextField()
    status = models.CharField(max_length=50)
    tagline = models.TextField() 
    adult = models.BooleanField()  
    
    # 추천용 N:M필드
    genres = models.ManyToManyField(Genre, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    directors = models.ManyToManyField(Director, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)


class Review(models.Model):
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_review')
    like_count = models.IntegerField(default=0)

# 리뷰 좋아요
class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')

class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment')



class Wishlist(models.Model):   # 보고싶은 영화
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('movie', 'user')

class View(models.Model):   # 본 영화
    view_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)