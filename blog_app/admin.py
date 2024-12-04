from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog_app.models import User, Blog
# Register your models here.

class UserAdimn(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

admin.site.register(User, UserAdimn)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category']

    def author(self, obj):
        return obj.author.username
