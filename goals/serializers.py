from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from core.models import User
from core.serializers import ProfileSerializer
from goals.models import GoalCategory, GoalComment, Board, BoardParticipant
from goals.models import Goal

from django.db import transaction



class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated', 'is_deleted')
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=BoardParticipant.editable_roles)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardWithParticipantsSerializer(BoardSerializer):
    participants = ParticipantSerializer(many=True)

    def update(self, instance: Board, validated_data: dict):
        request_user: User = self.context['request'].user

        with transaction.atomic():
            Board.objects.filter(board=instance).exclude(user=request_user).delete()
            participants = [
                BoardParticipant(user=participant['user'], role=participant['role'], board=instance)
                for participant in validated_data.get('participants', )
            ]
            BoardParticipant.objects.bulk_create(participants, ignore_conflicts=True)

            if title := validated_data.get('title'):
                instance.title = title
            instance.save()
            
        return instance
        #
        #
        # owner = validated_data.pop("user")
        # new_participants = validated_data.pop("participants")
        # new_by_id = {part["user"].id: part for part in new_participants}
        #
        # old_participants = instance.participants.exclude(user=owner)
        # with transaction.atomic():
        #     for old_participant in old_participants:
        #         if old_participant.user_id not in new_by_id:
        #             old_participant.delete()
        #         else:
        #             if (
        #                     old_participant.role
        #                     != new_by_id[old_participant.user_id]["role"]
        #             ):
        #                 old_participant.role = new_by_id[old_participant.user_id][
        #                     "role"
        #                 ]
        #                 old_participant.save()
        #             new_by_id.pop(old_participant.user_id)
        #     for new_part in new_by_id.values():
        #         BoardParticipant.objects.create(
        #             board=instance, user=new_part["user"], role=new_part["role"]
        #         )
        #
        #     if title := validated_data.get('title'):
        #         instance.title = title
        #     instance.save()
        #
        # return instance


    # class BoardView(RetrieveUpdateDestroyAPIView):
    #     model = Board
    #     permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    #     serializer_class = BoardSerializer
    #
    #     def get_queryset(self):
    #         # Обратите внимание на фильтрацию – она идет через participants
    #         return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
    #
    #     def perform_destroy(self, instance: Board):
    #         # При удалении доски помечаем ее как is_deleted,
    #         # «удаляем» категории, обновляем статус целей
    #         with transaction.atomic():
    #             instance.is_deleted = True
    #             instance.save()
    #             instance.categories.update(is_deleted=True)
    #             Goal.objects.filter(category__board=instance).update(
    #                 status=Goal.Status.archived
    #             )
    #         return instance



class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_board(self, board: Board) -> Board:
        if board.is_deleted:
            raise ValidationError('Board not exists')

        if not BoardParticipant.objects.filter(
            board_id=board.id,
            user_id=self.context['request'].user.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists():
            raise PermissionDenied

        return board

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')
        fields = '__all__'


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
#
#     class Meta:
#         model = GoalCategory
#         read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')
#         fields = '__all__'
#
#
class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError('Category not found')
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, category: GoalCategory):
        if category.is_deleted:
            raise ValidationError('category not exists')

        if not BoardParticipant.objects.filter(
                board_id=category.board_id,
                user_id=self.context['request'].user.id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists():
            raise PermissionDenied

        return category


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_goal(self, goal: Goal):
        if goal.status == Goal.Status.archived:
            raise ValidationError('Goal not exists')

        if not BoardParticipant.objects.filter(
                board_id=goal.category.board_id,
                user_id=self.context['request'].user.id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists():
            raise PermissionDenied

        return goal


class GoalCommentSerializer(GoalCommentCreateSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')
        fields = '__all__'

    # def validate_goal(self, value: Goal):
    #     if value.status == Goal.Status.archived:
    #         raise ValidationError('Goal not found')
    #     if self.context['request'].user.id != value.user_id:
    #         raise PermissionDenied
    #     return value
