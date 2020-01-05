import pandas as pd


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




if __name__ == '__main__':
    df = pd.read_csv("../../webapp/datasets/tips.csv")

    n = get_all_features(data=df)

    print(n)
