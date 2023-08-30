from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic 
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from django.utils import timezone 

from .serializers import *
from .models import Account, Category, CategoryItem
from .tasks import *

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'correlation/index.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return Category.objects.order_by('-created_date')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = self.queryset
        category = self.kwargs['category']
        if category is not None:
            queryset = CategoryItem.objects.filter(category=category).order_by('created_date')
        return queryset 

    def create(self, request):
        data = {
            "account": request.user.pk,
            "name": request.data["name"],
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CategoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryItemSerializer
    queryset = CategoryItem.objects.all()
    
    def get_queryset(self):
        return super().get_queryset()

    def create(self, request):
        data = request.data

        record_type = data.get('record_type')
        print('===========CategoryItem create()===========')
        print('input record_type: ' + record_type)
        print('===========================================')
        if record_type == CategoryItem.RecordType.EXISTENCE.label:
            data['record_type'] = CategoryItem.RecordType.EXISTENCE
        elif record_type == CategoryItem.RecordType.STRENGTH.label:
            data['record_type'] = CategoryItem.RecordType.STRENGTH
        elif record_type == CategoryItem.RecordType.TIME.label:
            data['record_type'] = CategoryItem.RecordType.TIME
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryItemListViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryItemSerializer

    def get_queryset(self):
        category = self.kwargs['category_id']

        return CategoryItem.objects.filter(
            category=category
        ).order_by('created_date')

class CategoryItemDataListViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryItemDataSerializer

    def get_queryset(self):
        category_item = self.kwargs['category_item_id']

        return CategoryItemData.objects.filter(category_item=category_item).order_by('created_date')
    

class CategoryItemDataViewSet(viewsets.ModelViewSet):
    queryset = CategoryItemData.objects.all()
    serializer_class = CategoryItemDataSerializer

    def get_queryset(self):
        category_item = self.kwargs['category_item_id']

        return CategoryItemData.objects.filter(
            category_item=category_item
        ).order_by('created_date')

    def create(self, request, *args, **kwargs):
        data = request.data
        category_item = data.get('category_item')

        try:
            category_item = CategoryItem.objects.get(pk=category_item)
        except:
            raise NotFound("not found")
        
        data['category_item'] = category_item.pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StatisticsAnalazingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StatisticsAnlazingSerializer
    def post(self, request):
        data = request.data

        if not CategoryItem.objects.filter(id=data.get('category_item_x')).exists():
            return JsonResponse({'msg': 'CATEGORY_ITEM_DOES_NOT_EXISTS'}, status=404)
        x = CategoryItem.objects.get(id=data.get('category_item_x'))
        if not CategoryItem.objects.filter(id=data.get('category_item_y')).exists():
            return JsonResponse({'msg': 'CATEGORY_ITEM_DOES_NOT_EXISTS'}, status=404)
        y = CategoryItem.objects.get(id=data.get('category_item_y'))

        result = test_correof_x_y(x, y, data.get('target_year'), data.get('target_month'))

        serializer = self.serializer_class(data=data, context={'content': result, 'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class StatisticsPredictView(APIView):
    permission_classes = []
    serializer_class = StatisticsPredictSerializer

    def post(self, request):
        data = request.data 
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        category_item_x = serializer.validated_data['category_item_x']
        category_item_y = serializer.validated_data['category_item_y']
        x_setting = serializer.validated_data['x_setting']

        predicted_y = predict_y_for_x(category_item_x, category_item_y, x_setting, 2023, 8)
        return JsonResponse({'predicted_y': predicted_y}, status=status.HTTP_201_CREATED)

class TestPandasView(View):
    def get(self, request, categoryitem1_id, categoryitem2_id):
        if not CategoryItem.objects.filter(id=categoryitem1_id).exists():
            return JsonResponse({'msg': 'CATEGORY_ITEM_DOES_NOT_EXISTS'}, status=404)
        category_item1 = CategoryItem.objects.get(id=categoryitem1_id)

        if not CategoryItem.objects.filter(id=categoryitem2_id).exists():
            return JsonResponse({'msg': 'CATEGORY_ITEM_DOES_NOT_EXISTS'}, status=404)
        category_item2 = CategoryItem.objects.get(id=categoryitem2_id)

        test_correof_x_y(x=category_item1, y=category_item2)



    

