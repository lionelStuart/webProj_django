from django.contrib import admin

# Register your models here.
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    # 过滤返回结果
    list_filter = ('status', 'created', 'publish', 'author')
    # 定义搜索字段
    search_fields = ('title', 'body')
    # 自动填充标题
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    # 快速导航
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
