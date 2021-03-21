from django.contrib.auth.models import User, Group
from rest_framework import serializers
from menu.models import Cart, CartContent


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']




class CartSerializer(serializers.HyperlinkedModelSerializer):
    cart_content = serializers.SerializerMethodField(source='get_cart_content')
    user = UserSerializer

    # def get_cart_content(self, cart):
    #     return CartContent.objects.filter(cart=cart)

    class Meta:
        model = Cart
        fields = ['cart_content', 'user', 'product']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
