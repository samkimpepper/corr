from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views 

router = DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('categoryitem', views.CategoryItemViewSet)
#router.register('category/item-list/<int:category_id>', views.CategoryItemListViewSet)
router.register('account', views.AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('category/item-list/<int:category_id>', views.CategoryItemListViewSet.as_view({'get': 'list'})),
    path('pandas/<int:categoryitem1_id>/<int:categoryitem2_id>/', views.TestPandasView.as_view(), name='test_pandas'),
    
]