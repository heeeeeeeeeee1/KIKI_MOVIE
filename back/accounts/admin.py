from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 사용자 정보 수정 화면에 추가 필드 표시
    fieldsets = (
        ("Infos", {
            "fields": ("email", "password", "username", "gender", "birth_date", "introduce"),  # 추가할 필드
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
            "classes": ("collapse", ),
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse", ),
        })
    )
    # 유저 추가 시 나타나는 폼 커스터마이징
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "gender", "birth_date", "introduce"),  # 추가 필드
        }),
    )

    # 리스트 화면에서 표시할 필드 및 정렬 설정
    list_display = ('username', 'email', 'gender', 'birth_date', 'is_staff')
    list_filter = ('gender', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)