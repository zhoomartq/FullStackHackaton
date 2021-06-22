from django.contrib import admin

from products.models import Product, Comment, Favorite

admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Favorite)
