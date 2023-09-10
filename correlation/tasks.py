from decimal import Decimal

import pandas as pd 
from sklearn.linear_model import LinearRegression
import numpy as np 
from scipy.stats import pearsonr
from datetime import date, timedelta
from django.db.models import Q 

from .models import Category, CategoryItem, CategoryItemData

import datetime

def calculate_target_date(year, month):
    start_month = month
    end_month = month

    if month is None:
        start_month = 1
        end_month = 11
        
    start_date = date(year, start_month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, end_month + 1, 1)

    return start_date, end_date

def correof_x_y(x, y):
    x_data_list = CategoryItemData.objects.filter(category_item=x).order_by('created_date')
    y_data_list = CategoryItemData.objects.filter(category_item=y).order_by('created_date')

    common_dates = set(x_data_list.values_list('created_date', flat=True)).intersection(
        set(y_data_list.values_list('created_date', flat=True))
    )

    x_values = []
    y_values = []
    print(f"***common dates: {common_dates}")

    for date in common_dates:
        x_value = x_data_list.get(created_date=date).figure
        y_value = y_data_list.get(created_date=date).figure 
        x_values.append(x_value)
        y_values.append(y_value)

    dataframe = {
        'x': x_values,
        'y': y_values
    }

    df = pd.DataFrame(dataframe)

    corr_coef, p_value = pearsonr(df['x'], df['y'])
    
    comment_corr = f"상관관계는 {corr_coef}입니다. "
    comment_desc = ""

    if p_value < 0.05:
        if abs(corr_coef) >= 0.7:
            comment_desc = "상당히 강한 상관관계가 있습니다"
        elif abs(corr_coef) >= 0.5:
            comment_desc = "어느 정도의 상관관계가 있습니다"
        else:
            comment_desc = "약한 상관관계가 있습니다. "
    else:
        comment_desc = "유의미하지 않습니다"

    return  comment_corr + comment_desc
        

#한 달간의 데이터만 계산
def test_correof_x_y(x, y, year, month):
    start_date, end_date = calculate_target_date(year, month)
    
    x_data_list = CategoryItemData.objects.filter(
        Q(category_item=x) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
    ).order_by('created_date')

    y_data_list = CategoryItemData.objects.filter(
        Q(category_item=y) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
    ).order_by('created_date')

    date_table = []
    date = datetime.date(year, month, 1)

    x_value_table = []
    y_value_table = []
    x_idx = 0
    y_idx = 0
    day_diff = end_date - start_date
    for _ in range(0, day_diff.days):
        date_table.append(date)

        if x_idx < len(x_data_list) and x_data_list[x_idx].created_date == date :
            x_value_table.append(x_data_list[x_idx].figure)
            x_idx += 1
        else:
            x_value_table.append(0)

        if y_idx < len(y_data_list) and y_data_list[y_idx].created_date == date :
            y_value_table.append(y_data_list[y_idx].figure)
            y_idx += 1 
        else:
            y_value_table.append(0)

        date = date + datetime.timedelta(days=1)

    
    dataframe = {'date': date_table,
                 'x': x_value_table,
                 'y': y_value_table}

    df = pd.DataFrame(dataframe)
    print(df)
    corr_coef, p_value = pearsonr(df['x'], df['y'])
    print(f"corr_coef: {corr_coef}")
    
    #corr_coef = df['x'].corr(df['y'], method='pearson')
    comment = ""

    if p_value < 0.05:
        if abs(corr_coef) >= 0.7:
            comment = "상당히 강한 상관관계가 있습니다"
        elif abs(corr_coef) >= 0.5:
            comment = "어느 정도의 상관관계가 있습니다"
        else:
            comment = "약한 상관관계가 있습니다. "
    else:
        "유의미하지 않습니다"
    print(comment)
    return comment 


def predict_y_for_x(x, y, x_setting, year, month):
    start_date, end_date = calculate_target_date(year, month)
    
    x_data_list = CategoryItemData.objects.filter(
        Q(category_item=x) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
    ).order_by('created_date')

    y_data_list = CategoryItemData.objects.filter(
        Q(category_item=y) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
    ).order_by('created_date')

    date_table = []
    date = datetime.date(year, month, 1)

    x_value_table = []
    y_value_table = []
    x_idx = 0
    y_idx = 0
    day_diff = end_date - start_date
    for _ in range(0, day_diff.days):
        date_table.append(date)

        if x_idx < len(x_data_list) and x_data_list[x_idx].created_date == date :
            x_value_table.append(x_data_list[x_idx].figure)
            x_idx += 1
        else:
            x_value_table.append(0)

        if y_idx < len(y_data_list) and y_data_list[y_idx].created_date == date :
            y_value_table.append(y_data_list[y_idx].figure)
            y_idx += 1 
        else:
            y_value_table.append(0)

        date = date + datetime.timedelta(days=1)

    
    dataframe = {'date': date_table,
                 'x': x_value_table,
                 'y': y_value_table}

    df = pd.DataFrame(dataframe)
    X = df['x'].values.reshape(-1, 1)
    y = df['y'].values 

    model = LinearRegression()
    model.fit(X, y)

    tomorrow_consumption = [[x_setting]]
    predicted = model.predict(tomorrow_consumption)
    print(predicted)
    return np.round(predicted, decimals=2).tolist()
    
def mean_x(x, year, month):
    start_date, end_date = calculate_target_date(year, month)

    x_data_list = CategoryItemData.objects.filter(
        Q(category_item=x) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
    ).order_by('created_date')

    date_table = []
    date = datetime.date(year, month, 1)

    x_value_table = []
    x_idx = 0
    day_diff = end_date - start_date
    for _ in range(0, day_diff.days):
        date_table.append(date)

        if x_idx < len(x_data_list) and x_data_list[x_idx].created_date == date :
            x_value_table.append(x_data_list[x_idx].figure)
            x_idx += 1
        else:
            x_value_table.append(0)

        date = date + datetime.timedelta(days=1)
    
    dataframe = {'date': date_table,
                 'x': x_value_table,
                }

    df = pd.DataFrame(dataframe)
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.dayofweek

    mean_day_of_week = df.groupby('day_of_week')['x'].mean()
    mean_month = df['x'].mean()

    return mean_month

def compare_mean(curr_mean, prev_mean):
    curr_mean = Decimal(str(curr_mean))

    percent_change = ((curr_mean - prev_mean) / prev_mean) * 100
    
    return percent_change
        
    