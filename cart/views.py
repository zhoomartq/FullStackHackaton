from rest_framework import viewsets

from . import permissions
from .models import Cart
from .permissions import IsOwnerOrReadOnly, IsCustomerPermission, IsAuthorPermission
from .serializers import CartSerializer
from rest_framework import permissions




# class CartViewSet(viewsets.ModelViewSet):
#     queryset = Cart.objects.all().order_by('-id')
#     serializer_class = CartSerializer
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         IsOwnerOrReadOnly
#     )
#
#     def get_queryset(self):
#         user = self.request.user.id
#         queryset = self.queryset.filter(user=user)
#         return queryset
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user.id)



class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsCustomerPermission, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class CartViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        qs = self.request.user.id
        queryset = super().get_queryset()
        queryset = queryset.filter(user=qs)
        return queryset
