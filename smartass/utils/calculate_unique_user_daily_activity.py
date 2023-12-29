import pandas as pd

def calculate_unique_user_daily_activity( user_id_timestamp_dataframe ):
    #i have limited time. so i didnt make here fp paradigm
    
    user_id_timestamp_dataframe['timestamp'] = pd.to_datetime(user_id_timestamp_dataframe['timestamp'], unit='s')
    result = user_id_timestamp_dataframe.groupby(user_id_timestamp_dataframe['timestamp'].dt.date)['user_id'].nunique().reset_index()
    result.columns = ['x', 'y']

    return result