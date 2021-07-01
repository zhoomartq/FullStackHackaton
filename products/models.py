from django.db import models

from user.models import CustomUser



# class Category(models.Model):
#     slug = models.SlugField(primary_key=True, max_length=50)
#     name = models.CharField(max_length=250)
#     parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
#
#     def __str__(self):
#         if self.parent:
#             return f'{self.parent} ... {self.name}'
#         return self.name
#
#     class Meta:
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#
#     @property
#     def get_children(self):
#         if self.children:
#             return self.children.all()
#         return False


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    # date = models.DateTimeField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}--{self.body[0:10]}'

    class Meta:
        ordering = ('created',)


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} added to favorite'


class Like(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} - {self.product}'
