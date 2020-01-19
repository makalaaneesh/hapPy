import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def load_data():
    depressed_data = pd.read_csv('preprocessed_depression_posts.csv')
    control_group_data = pd.read_csv('preprocessed_control_group_posts.csv')

    depressed_data['depressed'] = 1
    depressed_data = depressed_data[['text', 'depressed']]

    control_group_data['depressed'] = 0
    control_group_data = control_group_data[['text', 'depressed']]

    all_data = pd.concat([control_group_data, depressed_data])
    x = all_data[['text']]
    y = all_data['depressed']

    return x, y


def split_data(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                        test_size=0.33, random_state=42)
    return x_train, x_test, y_train, y_test


