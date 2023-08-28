import pandas as pd 
import numpy as np 
from scipy.stats import pearsonr
from datetime import date
from django.db.models import Q 

from .models import Category, CategoryItem, CategoryItemData

import datetime

def calculate_target_date(year, month):
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    return start_date, end_date

#한 달간의 데이터만 계산
def test_correof_x_y(x, y, year, month):
    print(x.name)
    #x_data_list = CategoryItemData.objects.order_by('recorded_date').filter(category_item=x)
    start_date, end_date = calculate_target_date(year, month)
    
    x_data_list = CategoryItemData.objects.filter(
        Q(category_item=x) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
    ).order_by('created_date')

    y_data_list = CategoryItemData.objects.filter(
        Q(category_item=y) & Q(created_date__gte=start_date) & Q(created_date__lt=end_date)
    ).order_by('-created_date')

    date_table = []
    date = datetime.date(year, month, 1)

    x_value_table = []
    y_value_table = []
    x_idx = 0
    y_idx = 0
    for _ in range(0, 30):
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
    #corr_coef = df['x'.corr(df['y'], method='pearson')]
    corr_coef, p_value = pearsonr(df['x'], df['y'])
    print(corr_coef)

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

    return comment 



    # 여기서 StatisticsResult 내용도 만들면 좋을텐데. 
    # 만약 똑같은 x,y에 대한 전월 데이터가 있다면 그것도 비교하면 좋을텐데. 



    
    