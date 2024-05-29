import pandas as pd
import numpy as np
from datetime import timedelta
import os
import matplotlib.pyplot as plt
pd.options.mode.copy_on_write = True



def get_dataframes(print_names=True):
    data = {}
    data_path = './data'
    for csv_file in os.listdir(data_path):
        data[csv_file.replace('.csv', '')] = pd.read_csv(data_path+'/'+csv_file, low_memory=False)
        if print_names:
            print(csv_file.replace('.csv', ''))
    data['RPM_DOW_2023_10min_avg'] = data['RPM_DOW_2023_10min_avg'].ffill()
    data['yaw_angle_DOW_2023_10min_avg'] = data['yaw_angle_DOW_2023_10min_avg'].ffill()
    data['wind_direction_DOW_2023_10min_avg'] = data['wind_direction_DOW_2023_10min_avg'].ffill()
    return data

def timestamp_to_datetime_index(df):
    if 'timestamp' not in df.columns:
        raise KeyError('timestamp not in dataframe')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    return df



def calculate_TI(ws_df, interval = 10):
    bin_delta = timedelta(minutes=interval)
    is_series = False
    try:
        ws_column = [s for s in ws_df.columns if 'WindSpeed' in s][0]
    except:
        if 'WindSpeed' in ws_df.name:
            ws_column = ws_df.name
            is_series = True
        else:
            raise KeyError('No windspeed column found')
        
    TI_label = ws_column.replace('WindSpeed', 'TI')

    def calculate_rolling_TI_std():
        if is_series:
            mean = ws_df.rolling(window = bin_delta, min_periods = 50).mean()
            std = ws_df.rolling(window = bin_delta, min_periods = 50).std()
            ti = std/mean
            ti = ti.rename(TI_label)

        else:
            mean = ws_df[ws_column].rolling(window = bin_delta, min_periods = 50).mean()
            std = ws_df[ws_column].rolling(window = bin_delta, min_periods = 50).std()
            ti = std/mean
            ti = ti.rename(columns = {ws_column: TI_label})
        return ti
    
    ti = calculate_rolling_TI_std()
    return ti



def get_mean_TI_points():
    raw_data = get_dataframes(print_names=False)['RAW_Windspeed_DOW_4_Nov_2023'].pivot(index='source_timestamp', columns='tag', values='double_value')
    raw_data = raw_data.reset_index()
    raw_data = raw_data.rename(columns = {'source_timestamp': 'timestamp'})
    raw_data = timestamp_to_datetime_index(raw_data)

    J04_raw_ws = raw_data['DOW-J04-WindSpeed'].dropna()
    T05_raw_ws = raw_data['DOW-T05-WindSpeed'].dropna()
    J05_raw_ws = raw_data['DOW-J05-WindSpeed'].dropna()
    K05_raw_ws = raw_data['DOW-K05-WindSpeed'].dropna()
    L05_raw_ws = raw_data['DOW-L05-WindSpeed'].dropna()
    L04_raw_ws = raw_data['DOW-L04-WindSpeed'].dropna()

    T05_TI = calculate_TI(ws_df=T05_raw_ws)
    J04_TI = calculate_TI(ws_df=J04_raw_ws)
    J05_TI = calculate_TI(ws_df=J05_raw_ws)
    K05_TI = calculate_TI(ws_df=K05_raw_ws)
    L05_TI = calculate_TI(ws_df=L05_raw_ws)
    L04_TI = calculate_TI(ws_df=L04_raw_ws)

    ti_ws = pd.merge(J04_raw_ws, J04_TI, on='timestamp', how='outer').dropna()
    ti_ws_addon = pd.merge(T05_raw_ws, T05_TI, on='timestamp', how='outer').dropna().rename(columns={'DOW-T05-WindSpeed':'DOW-J04-WindSpeed', 'DOW-T05-TI':'DOW-J04-TI'})
    ti_ws_addon1 = pd.merge(J05_raw_ws, J05_TI, on='timestamp', how='outer').dropna().rename(columns={'DOW-J05-WindSpeed':'DOW-J04-WindSpeed', 'DOW-J05-TI':'DOW-J04-TI'})
    ti_ws_addon2 = pd.merge(K05_raw_ws, K05_TI, on='timestamp', how='outer').dropna().rename(columns={'DOW-K05-WindSpeed':'DOW-J04-WindSpeed', 'DOW-K05-TI':'DOW-J04-TI'})
    ti_ws_addon3 = pd.merge(L05_raw_ws, L05_TI, on='timestamp', how='outer').dropna().rename(columns={'DOW-L05-WindSpeed':'DOW-J04-WindSpeed', 'DOW-L05-TI':'DOW-J04-TI'})
    ti_ws_addon4 = pd.merge(L04_raw_ws, L04_TI, on='timestamp', how='outer').dropna().rename(columns={'DOW-L04-WindSpeed':'DOW-J04-WindSpeed', 'DOW-L04-TI':'DOW-J04-TI'})

    ti_ws=  pd.concat([ti_ws, ti_ws_addon, ti_ws_addon1, ti_ws_addon2, ti_ws_addon3, ti_ws_addon4], ignore_index=True)

    ti_ws['ws_bins'] = pd.cut(ti_ws['DOW-J04-WindSpeed'], 30)
    ws_x = ti_ws.groupby('ws_bins', observed=True)['DOW-J04-WindSpeed'].mean().to_numpy()
    ti_y = ti_ws.groupby('ws_bins', observed=True)['DOW-J04-TI'].mean().to_numpy()
    return ws_x, ti_y

ws_x, ti_y = get_mean_TI_points()
degree = 3
coefficients = np.polyfit(ws_x, ti_y, degree)
poly_func = np.poly1d(coefficients)

def ws2ti_0(ws):
    return poly_func(ws)


def plot_ti_polynomial():
    ws_x, ti_y = get_mean_TI_points()
    x_fit = np.linspace(min(ws_x), max(ws_x), 100)
    y_fit = ws2ti_0(x_fit)

    # Plot the original data and the fitted function
    plt.scatter(ws_x, ti_y, label='Mean Data Points')
    plt.plot(x_fit, y_fit, color='red', label='Fitted Polynomial')
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('TI')
    plt.legend()
    plt.title('Fitted Ti curve')


