import pandas as pd
import matplotlib as plt
import seaborn as sns
import numpy as np
import re


def create_df_with_datetime(file_name):
    df = pd.read_csv(f'/kaggle/input/ipl2020-tweets/{file_name}.csv')
#     df = pd.read_csv('/kaggle/input/new-york-city-transport-statistics/mta_1706.csv')
    return df


# Read the data set
df1 = create_df_with_datetime("IPL2020_Tweets")
# df2 = pd.read_csv('/kaggle/input/ipl2020-tweets/IPL_2021_tweets.csv')
# df3 = create_df_with_datetime("IPL_2022_tweets")


# Drop NULL values rows
df1 = df1.dropna()


# Specify the column name to check for non-English characters
column_name_1 = 'user_name'
column_name_2 = 'user_location'
column_name_3 = 'text'
columns = [column_name_1, column_name_2, column_name_3]


def remove_non_english_rows(df1):
    non_english_pattern = re.compile(r'[^\x00-\x7F]+')

    rows_to_drop = []

    for index, row in df1.iterrows():
        for column in columns:
            text = str(row[column])

            if non_english_pattern.search(text):
                rows_to_drop.append(index)

    df1.drop(rows_to_drop, inplace=True)
    return df1


remove_non_english_rows(df1)

df1.to_csv('/kaggle/working/english_tweets_text.csv', index=False)