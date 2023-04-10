from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)

from django.shortcuts import get_object_or_404

from posts.models import Post, Group, User
from .serializers import (PostSerializer, GroupSerializer,
                          CommentSerializer, FollowSerializer)
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    '''View функция для создания и отображения постов.'''
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        '''Определенный пользователь создает пост'''
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    '''View функция для отображения групп.'''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    '''View функция для создания и отображения комментариев.'''
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_post(self):
        '''Получаем пост.'''
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post

    def get_queryset(self):
        '''Получаем все комменты под постом'''
        new_queryset = self.get_post().comments.all()
        return new_queryset

    def perform_create(self, serializer):
        '''Создаем коммент под постом'''
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        '''Получаем список, на кого подписан пользователь'''
        user = get_object_or_404(User, username=self.request.user)
        following = user.follower.all()
        return following

    def perform_create(self, serializer):
        '''Создаем подписку на другого автора'''
        serializer.save(user=self.request.user)
