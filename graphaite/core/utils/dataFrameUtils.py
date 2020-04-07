import pandas as pd
import pathlib
from enum import Enum

class FeatureType(Enum):
    CATEGORICAL  = 1
    NUMERICAL  = 2
    TIMESERIES = 3



def get_numeric_features(data, uniqueness_threshold=0.05):
    """
    Given a pandas DataFrame, retuns the list of numeric columns from it.

    :param data: (pandas DataFrame), the target dataset
    :param uniqueness_threshold: (float), the uniqueness of occurance to treat numeric labeled feature to exclude from numeric
    :return: (list) list of numeric columns in the DataFrame
    """

    num_cols = data._get_numeric_data().columns

    # finding out numeric labeled categorical features 
    # Reference: https://stackoverflow.com/questions/35826912/what-is-a-good-heuristic-to-detect-if-a-column-in-a-pandas-dataframe-is-categori
    likely_categorical = []
    for var in num_cols:
        unique_values_ratio = 1.*data[var].nunique()/data[var].count()

        if unique_values_ratio < uniqueness_threshold:
            likely_categorical.append(var)


    return list(set(num_cols) - set(likely_categorical))


def get_categorical_features(data, uniqueness_threshold=0.05):
    """
    Given a pandas DataFrame, retuns the list of categorical columns from it.

    :param data: (pandas DataFrame), the target dataset
    :param uniqueness_threshold: (float), the uniqueness of occurance to treat numeric labeled feature to exclude from numeric
    :return: (list) list of categorical columns in the DataFrame
    """

    all_columns_set = set(data.columns)
    numeric_columns_set = set(get_numeric_features(data=data, uniqueness_threshold=uniqueness_threshold))

    return list(all_columns_set - numeric_columns_set)


def get_all_features(data):
    """
    Given a Pandas DataFrame, returns all its column names.

    :param data: (Pandas DataFrame), the target DataFrame
    :return: (list) list of all the column names in the DataFrame
    """

    return list(data.columns)


def get_feature_type(data, target_feature)->str:
    """ Returns the type of the supplied feature. Such as, Categorical, Neumerical, TimeSeries.

    Args:
        data (Pandas DataFrame): The target DataFrame   
        target_feature (string, column name): the target feature to detect and return type of.

    Returns:
        str: ""    
    """

    if target_feature not in get_all_features(data):
        return None

    if target_feature in get_numeric_features(data):
        return FeatureType.NUMERICAL
    elif target_feature in get_categorical_features(data):
        return FeatureType.CATEGORICAL
    
    ## TODO: Add Time series data type

    return None



if __name__ == '__main__':
    WEBAPP_DIR = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/webapp/"

    df = pd.read_csv(WEBAPP_DIR+"/datasets/titanic.csv")

    print(get_numeric_features(df))
    print(get_categorical_features(df))

    print(get_feature_type(df, "sex") == get_feature_type(df, "survived"))

    print(FeatureType.CATEGORICAL == FeatureType.NUMERICAL)

    # n = get_all_features(data=df)

    # dataType = get_feature_type(data=df, target_feature="sex")

    # print(dataType)
