from rest_framework import serializers
from datetime import datetime, time
from enum import Enum
from .models import *
from account.serializers import *

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'account')

    def create(self, validated_data):
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
        fields = ('category_item', 'figure', 'created_date')

    def create(self, validated_data):
        category_item_data = CategoryItemData.objects.create(**validated_data)
        return category_item_data
    
class StatisticsAnlazingSerializer(serializers.Serializer):
    category_item1 = serializers.PrimaryKeyRelatedField(queryset=CategoryItem.objects.all())
    category_item2 = serializers.PrimaryKeyRelatedField(queryset=CategoryItem.objects.all())
    
    class DateDigitEnum(Enum):
        MONTH = 'month'
        YEAR = 'year'
        ALL = 'all'

    date_digit = serializers.ChoiceField(choices=[(tag.name, tag.value) for tag in DateDigitEnum])
    year = serializers.IntegerField()
    month = serializers.IntegerField(allow_null=True)

    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("월은 1부터 12까지입니다.")
        return value 
    
    def create(self, validated_data):
        content = self.context.get('content')
        if content is None:
            raise ValueError("content가 없음")
        user = self.context.get('user')
        if user is None:
            raise ValueError("User가 없음")

        statistics_result = StatisticsResult(
            content=content,
            category_item_x=validated_data['category_item1'],
            category_item_y=validated_data['category_item2'],
            account=user,
            target_year=validated_data['year'],
            target_month=validated_data['month']
        )
        statistics_result.save()
        return statistics_result
    



    

