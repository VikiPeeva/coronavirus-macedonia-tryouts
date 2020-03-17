import pandas as pd


def get_data_by_country_name(data, country_column, country_name):
    return data.loc[data[country_column] == country_name]


def convert_data_in_day_count_larger_than_zero_format(data, id_vars, value_vars, var_name, value_name):
    converted = pd.melt(data, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)
    converted = converted.loc[converted[value_name] > 0].reset_index(drop=True)
    converted.insert(0, 'artificial_day', range(1, 1 + len(converted)))
    return converted.loc[converted[value_name] > 0].reset_index(drop=True)
