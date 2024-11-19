from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 사용자 정보 수정 화면에 추가 필드 표시
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {  # 새 섹션 이름
            'fields': ('gender', 'birth_date', ),  # 추가할 필드
        }),
    )

    # 사용자 생성 화면에 추가 필드 표시
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('추가 정보', {
            'classes': ('wide',),
            'fields': ('gender', 'birth_date', 'email', ),
        }),
    )

    # 리스트 화면에서 표시할 필드
    list_display = ('username', 'email', 'gender', 'birth_date', 'is_staff')
    list_filter = ('gender', 'is_staff', 'is_superuser')
	