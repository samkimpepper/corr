from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views 

#app_name = 'correlation'

router = DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('categoryitem', views.CategoryItemViewSet)
router.register('categoryitemdata', views.CategoryItemDataViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('category/item-list/<int:category_id>', views.CategoryItemListViewSet.as_view({'get': 'list'})),
    path('category/data-list/<int:category_item_id>', views.CategoryItemDataListViewSet.as_view({'get': 'list'})),
    path('statistics/correof/', views.StatisticsAnalazingView.as_view(), name='correof'),
    path('statistics/predict/', views.StatisticsPredictView.as_view(), name='predict'),
    path('pandas/<int:categoryitem1_id>/<int:categoryitem2_id>/', views.TestPandasView.as_view(), name='test_pandas'),
    
]