import pandas as pd
import pathlib

def get_numeric_features(data):
    """
    Given a pandas DataFrame, retuns the list of numeric columns from it.

    :param data: (pandas DataFrame), the target dataset
    :return: (list) list of numeric columns in the DataFrame
    """

    num_cols = data._get_numeric_data().columns
    return list(num_cols)


def get_categorical_features(data):
    """
    Given a pandas DataFrame, retuns the list of categorical columns from it.

    :param data: (pandas DataFrame), the target dataset
    :return: (list) list of categorical columns in the DataFrame
    """

    all_columns_set = set(data.columns)
    numeric_columns_set = set(get_numeric_features(data=data))

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
        return "Numeric"
    elif target_feature in get_categorical_features(data):
        return "Categorical"
    
    ## TODO: Add TIme series data type

    return None



if __name__ == '__main__':
    WEBAPP_DIR = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/webapp/"

    df = pd.read_csv(WEBAPP_DIR+"/datasets/tips.csv")

    n = get_all_features(data=df)

    dataType = get_feature_type(data=df, target_feature="sex")

    print(dataType)
