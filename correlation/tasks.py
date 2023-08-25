import pandas as pd 
import numpy as np 
from .models import Category, CategoryItem, CategoryItemData

import datetime 

#한 달간의 데이터만 계산
def test_correof_x_y(x, y):
    print(x.name)
    x_data_list = CategoryItemData.objects.order_by('recorded_date').filter(category_item=x)
    y_data_list = CategoryItemData.objects.order_by('-recorded_date').filter(category_item=y)

    date_table = []
    target_year = x_data_list[0].recorded_date.year
    target_month = x_data_list[0].recorded_date.month 
    date = datetime.date(target_year, target_month, 1)
    datetime.date(2022, 1, 1)

    x_value_table = []
    y_value_table = []
    x_idx = 0
    y_idx = 0
    for day in range(0, 30):
        date_table.append(date)

        if x_idx < len(x_data_list) and x_data_list[x_idx].recorded_date == date :
            x_value_table.append(x_data_list[x_idx].figure)
            x_idx += 1
        else:
            x_value_table.append(0)

        if y_idx < len(y_data_list) and y_data_list[y_idx].recorded_date == date :
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

    print(df['x'].corr(df['y'], method='pearson'))
    # 여기서 StatisticsResult 내용도 만들면 좋을텐데. 
    # 만약 똑같은 x,y에 대한 전월 데이터가 있다면 그것도 비교하면 좋을텐데. 


    
    