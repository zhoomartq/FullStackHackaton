from rest_framework import serializers

from products.models import Product, Comment, Favorite, Like




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('owner', 'like')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.email
        return representation


class ProductSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'image',  'likes',)

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        action = self.context.get('action')
        likes = LikeSerializer(instance.likes.filter(like=True), many=True).data
        if action == 'list':
            representation['likes'] = {'like': likes}
            representation['likes'] = instance.likes.filter(like=True).count()
        if action == 'retrieve':
            representation['likes'] = likes
        return representation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body',)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
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




    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        review = Favorite.objects.create(user=user, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super(FavoriteSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation
