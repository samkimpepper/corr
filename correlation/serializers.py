from rest_framework import serializers

from .models import Account, Category, CategoryItem, CategoryItemData

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'username']

class CategorySerializer(serializers.ModelSerializer):
    account = AccountSerializer

    class Meta:
        model = Category
        fields = ('account', 'name',)

    def create(self, validated_data):
        #account = self.context.get('account', None)
        category = Category.objects.create(**validated_data)
        return category

class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem
        fields = ('category', 'name', 'record_type',)

    def create(self, validated_data):
        category_item = CategoryItem.objects.create(**validated_data)
        return category_item

    
class CategoryItemDataSerializer(serializers.ModelSerializer):
    category_item = CategoryItemSerializer

    class Meta:
        model = CategoryItemData
        fields = ('category_item', 'figure', 'recorded_time',)

    def create(self, validated_data):
        category_item = self.context['category_item']

        return CategoryItemData.objects.create(
            category_item=category_item, **validated_data
        )

    

