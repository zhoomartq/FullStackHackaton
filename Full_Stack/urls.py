from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from cart.views import CartViewSet
from products.views import CommentViewSet, ProductListView, chat

schema_view = get_schema_view(
    info=openapi.Info(
        title='TicketShop Project',
        default_version='v1',
        description='this is our ticket shop',
        terms_of_service='http://www.google.com/policies/terms/',
        contact=openapi.Contact(email='test@gmail.com'),
        license=openapi.License(name='BSD License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

router = DefaultRouter()
router.register('comment', CommentViewSet)
router.register('cart', CartViewSet)
router.register('products', ProductListView)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui()),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/accounts/', include('user.urls'),),
    path('api/v1/', include(router.urls)),
    path('social_auth/', include(('social_auth.urls', 'social_auth'), namespace="social_auth")),
    path('api/v1/chat/', chat),
]


urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
urlpatterns += static(
     settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
