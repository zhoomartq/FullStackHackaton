from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

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

urlpatterns = [
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui()),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/accounts/', include('user.urls'),),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
