from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from .filters import TitlesFilterBackend
from .mixins import (CreateListDestroyUpdateRetrieveViewSetMixin,
                     CreateListDestroyViewSetMixin)
from .permissions import IsAdmin
from .serializers import (CategorySerializer, Genre_titleSerializer,
                          GenreSerializer, SignUpSerializer, TitlesSerializer,
                          TitlesSerializerRetrieve, TokenSerializer,
                          UserMeSerializer, UserSerializer)
from .utils import send_confirmation_code
from reviews.models import Category, Genre, Genre_title, Titles
from users.models import User


class UserViewSet(ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username',)
    ordering = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')


class UserMeView(APIView):
    """Вью-функция для работы с текущим пользователем."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    """Вью-функция для регистрации и подтвержения по почте."""
    def post(self, request):
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            send_confirmation_code(request)
            return Response(request.data, status=HTTP_200_OK)

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_confirmation_code(request)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class Token(APIView):
    """Вью-функция для получения токена."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CategoryViewSet(CreateListDestroyViewSetMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSetMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class Genre_titleViewSet(viewsets.ModelViewSet):
    queryset = Genre_title.objects.all()
    serializer_class = Genre_titleSerializer


class TitleViewSet(CreateListDestroyUpdateRetrieveViewSetMixin):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, TitlesFilterBackend,)
    search_fields = ('genre__slug',)
    filterset_fields = ('genre', 'category', 'year', 'name')

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitlesSerializerRetrieve
        return TitlesSerializer
