from pandas.api.types import CategoricalDtype


def cat_to_int(df_train, df_test, col):
    catDtype = CategoricalDtype(categories=df_train[col].value_counts().index.values)
    return df_train[col].astype(catDtype).cat.codes.values, df_test[col].astype(catDtype).cat.codes.values