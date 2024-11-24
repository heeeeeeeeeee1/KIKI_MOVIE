from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=[('M', '남성'), ('W', '여성')], required=True)
    birth_date = serializers.DateField(required=True)

    def save(self, request):
        user = super().save(request)
        user.gender = self.validated_data.get('gender')
        user.birth_date = self.validated_data.get('birth_date')
        user.save()
        return user
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    # username 변경 못하게 막음
    username = serializers.CharField(read_only=True)
    # 추가 입력한 필드들
    gender = serializers.CharField()
    birth_date = serializers.DateField()
    introduce = serializers.CharField()

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'gender', 'birth_date', 'introduce')
