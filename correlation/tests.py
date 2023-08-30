from django.test import TestCase
from .models import *
from .tasks import *

# Create your tests here.
class PredictTaskTestCase(TestCase):
    def test_predict(self):
        x = CategoryItem.objects.filter(pk=2)
        y = CategoryItem.objects.filter(pk=1)
        start_date, end_date = calculate_target_date(2023, 8)
        x_data_list = CategoryItemData.objects.filter(
            Q(category_item=x) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
        ).order_by('created_date')

        y_data_list = CategoryItemData.objects.filter(
            Q(category_item=y) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
        ).order_by('created_date')



