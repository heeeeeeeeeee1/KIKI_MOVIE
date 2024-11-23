from django.contrib import admin
from .models import Movie, Genre, Actor, Keyword, Review, Comment

# 기존 모델 등록
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Keyword)

# 리뷰 모델 커스터마이징
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user', 'score', 'content', 'created_at')  # 목록에 표시할 필드
    list_filter = ('movie', 'user')  # 필터링 옵션
    search_fields = ('content', 'movie__title', 'user__username')  # 검색 가능 필드
    ordering = ('-created_at',)  # 생성일 기준 정렬

# 댓글 모델 등록 (필요 시)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'user', 'content', 'created_at')
    list_filter = ('review', 'user')
    search_fields = ('content', 'review__content', 'user__username')
    ordering = ('-created_at',)
