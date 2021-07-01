from django.contrib import admin

from products.models import Product, Comment, Favorite, Like

# admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Like)
