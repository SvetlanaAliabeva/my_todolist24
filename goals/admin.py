from django.contrib import admin

# Register your models here.
from django.contrib import admin

from goals.models import GoalCategory, Goal


# from goals.models import GoalComment
#
# from goals.models import Goal


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_deleted',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority')

#
# @admin.register(GoalComment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('text', 'user', 'goal')
#     search_fields = ('text', 'user__username', 'goal__title')
#     readonly_fields = ('created', 'updated')
#
#     fieldsets = (
#         ('Info', {
#             'fields': ('text', 'user', 'goal')
#         }),
#         ('Dates', {
#             'fields': ('created', 'updated')
#         }),
#     )
