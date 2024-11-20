from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework import status

from django.shortcuts import get_object_or_404, get_list_or_404

from .models import *
from .serializers import *


# 메인 페이지
def main(requset):
    pass


# 영화 단일(상세) 페이지 조회
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 영화 리뷰 페이지 조회
def movie_review(request, movie_pk, review_pk):
    pass