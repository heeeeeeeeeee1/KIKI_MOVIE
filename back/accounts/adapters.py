from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field

class CustomUserAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, False)  # 기본 동작 수행
        user_field(user, 'gender', request.data.get('gender'))
        user_field(user, 'birth_date', request.data.get('birth_date'))
        user_field(user, 'intorduce', request.data.get('intorduce'))
        if commit:
            user.save()
        return user
