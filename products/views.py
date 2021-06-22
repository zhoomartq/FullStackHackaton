from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.response import Response

from products import serializers
from products.models import Product, Favorite, Comment
from products.serializers import CommentSerializer, FavoriteSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        product = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user.CustomUser, product=product)
        if not created:
            obj.favorite = not obj.favorite
            obj.save()
        added_removed = 'added' if obj.favorite else 'removed'
        return Response('Successfully {} favorite'.format(added_removed), status=status.HTTP_200_OK)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser,)


class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductDestroyView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser,)


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser,)


class ProductSearchFilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
                Q(title__icontains=query) | Q(price__icontains=query) | Q(date__icontains=query)
            )
        return object_list


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        qs = self.request.user.profile_customer
        queryset = Favorite.objects.filter(user=qs, favorite=True)
        return queryset
