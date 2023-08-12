from django.urls import path

# from todolist.goals import views
from django.urls import path
from goals.apps import GoalsConfig
from goals.views.categories import CategoryCreateView, CategoryListViews, CategoryDetailView
from goals.views.goals import GoalListView, GoalsCreateVeiw, GoalDetailView
from goals.views.comments import GoalCommentListView, GoalCommentCreateView, GoalCommentDetailView

app_name = GoalsConfig.name


urlpatterns = [
    #
    path('goal_category/create', CategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', CategoryListViews.as_view(), name='category-list'),
    path('goal_category/<int:pk>', CategoryDetailView.as_view(), name='goal-category'),
    #
    path('goal/create', GoalsCreateVeiw.as_view(), name='create-goal'),
    path('goal/list', GoalListView.as_view(), name='goal-list'),
    path('goal/<int:pk>', GoalDetailView.as_view(), name='goal'),
    #
    path('goal_comment/create', GoalCommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='comment-list'),
    path('goal_comment/<int:pk>', GoalCommentDetailView.as_view(), name='comment'),
]
