from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from goals.models import GoalComment
from goals.permissions import GoalCommentPermission
from goals.serializers import GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCommentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer

class GoalCommentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class GoalCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCommentPermission]
    serializer_class = GoalCommentSerializer
    queryset = GoalComment.objects.select_related('user')

    def get_queryset(self):
        return GoalComment.objects.select_related('user').filter(
            goal__category__board__participants__user=self.request.user
        )
