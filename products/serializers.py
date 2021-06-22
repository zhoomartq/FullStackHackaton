from rest_framework import serializers

from products.models import Product, Comment, Favorite


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'product', 'body', )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user.profile_customer
        review = Comment.objects.create(user=user, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super(CommentSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'