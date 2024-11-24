from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=[('M', '남성'), ('W', '여성')], required=True)
    birth_date = serializers.DateField(required=True)

    def save(self, request):
        user = super().save(request)
        user.gender = self.validated_data.get('gender')
        user.birth_date = self.validated_data.get('birth_date')
        user.save()
        return user