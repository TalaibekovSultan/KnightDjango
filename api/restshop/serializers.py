from django.contrib.auth.models import User, Group
from rest_framework import serializers
from menu.models import Cart, CartContent, Menu, Company


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class CartSerializer(serializers.HyperlinkedModelSerializer):
    # def get_cart_content(self, cart):
    #     return CartContent.objects.filter(cart=cart)

    class Meta:
        model = Cart
        fields = '__all__'
        depth = 1

    def update(self, instance, validated_data):
        company = validated_data.pop('company', [])
        instance = super().update(instance, validated_data)
        for companys in company:
            instance.company.add(companys)
        instance.save()
        return instance


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CartContentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CartContent
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
