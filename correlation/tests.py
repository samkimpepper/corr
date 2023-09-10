from datetime import datetime 
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from rest_framework.reverse import reverse
from .models import *
from .tasks import *
from rest_framework.test import APITestCase, APIClient
import factory
from faker import Faker

from account.models import Account
from .tasks import *

# Create your tests here.

class CategoryViewSetTestCase(APITestCase):
    url = reverse('category-list')
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        req_data = {'name': 'Emotion'}
        res = self.client.post(self.url, req_data)
        self.assertEqual(201, res.status_code)
        self.assertEqual(1, Category.objects.count())

class CategoryItemViewSetTestCase(APITestCase):
    url = reverse('categoryitem-list')
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Emotion', account=self.user)
        
    def test_create_category_item(self):
        data = {"category": self.category.id, "name": "Anxiety", "record_type": "strength"}
        res = self.client.post(self.url, data)
        self.assertEqual(201, res.status_code)
        self.assertEqual(1, CategoryItem.objects.count())
        self.assertEqual(self.category, CategoryItem.objects.get().category)        

class CategoryItemDataViewSetTestCase(APITestCase):
    url = reverse('categoryitemdata-list')

    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Emotion', account=self.user)
        self.category_item = CategoryItem.objects.create(name='Anxiety', record_type=CategoryItem.RecordType.STRENGTH, category=self.category)

    def test_create_category_item_data(self):
        data = {"category_item": self.category_item.id, "figure": 3, "created_date": "2023-08-27"}
        res = self.client.post(self.url, data)
        self.assertEqual(201, res.status_code)
        self.assertEqual(datetime.date(2023, 8, 27), CategoryItemData.objects.get().created_date)

class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account
    username = factory.Faker('name')
    email = factory.Faker('email')
    password = 'password'

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    account = factory.SubFactory(AccountFactory)
    name = factory.Faker('word')
    created_date = factory.Faker('date_this_year')

class CategoryItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryItem

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker('word')
    created_date = factory.Faker('date_this_year')
    record_type = factory.Faker('random_element', elements=['strength'])

class CategoryItemDataXFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryItemData

    category_item = factory.SubFactory(CategoryItemFactory)
    figure = factory.Faker('pyint', min_value=0, max_value=5)
    created_date = factory.Iterator([datetime.datetime(2023, 1, 1) + timedelta(days=i) for i in range(100)])
    created_time = factory.Faker('time')

class CategoryItemDataYFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryItemData

    category_item = factory.SubFactory(CategoryItemFactory)
    figure = factory.Faker('pyint', min_value=0, max_value=5)
    created_date = factory.Iterator([datetime.datetime(2023, 1, 1) + timedelta(days=i) for i in range(100)])
    created_time = factory.Faker('time')

class TestFactory(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.category_item_x = CategoryItemFactory()
        self.category_item_y = CategoryItemFactory()

        for _ in range(30):
            CategoryItemDataXFactory(category_item=self.category_item_x)
            CategoryItemDataYFactory(category_item=self.category_item_y)

    def test_correof(self):
        url = reverse('correof')

        x = CategoryItemData.objects.filter(category_item=self.category_item_x)
        print(x[0].created_date)
        for i in x:
            print(i.created_date)
        y = CategoryItemData.objects.filter(category_item=self.category_item_y)
        print(y[0].created_date)

        data = {
            "category_item_x": self.category_item_x.id, 
            "category_item_y": self.category_item_y.id,
            "target_year": 2023,
            "target_month": 1
        }

        res = self.client.post(url, data)
        self.assertEqual(201, res.status_code)

    def test_predict(self):
        url = reverse('predict')

        data = {
            "category_item_x": self.category_item_x.id,
            "category_item_y": self.category_item_y.id,
            "x_setting": 0
        }

        res = self.client.post(url, data)
        print(res.content)
        self.assertEqual(200, res.status_code)

    def test_new_correof(self):
        result = correof_x_y(self.category_item_x, self.category_item_y)
        print(result)


        
class StatisticsMeanViewTestCase(APITestCase):
    url = reverse('mean')

    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)       

        self.category_item = CategoryItemFactory()

        for _ in range(60):
            CategoryItemDataXFactory(category_item=self.category_item)

    def test_mean(self):
        data = {
            "category_item": self.category_item.id,
            "target_year": 2023,
            "target_month": 1,
        }

        res = self.client.post(self.url, data)
        print(res.content)
        self.assertEqual(201, res.status_code)
        self.assertNotEqual(None, MonthlyMean.objects.get().mean)

    def test_mean_if_prev_exists(self):
        prev_data = {
            "category_item": self.category_item.id,
            "target_year": 2023,
            "target_month": 1,
        }
        res = self.client.post(self.url, prev_data)

        curr_data = {
            "category_item": self.category_item.id,
            "target_year": 2023,
            "target_month": 2,
        }
        res = self.client.post(self.url, curr_data)
        self.assertEqual(201, res.status_code)
        print(res.content)





