from dudgeon import NAMES
from util import timestamp_to_datetime_index, get_dataframes, ws2ti_0
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



data = get_dataframes(print_names=False)
data_labels = [('activepower_DOW_2023_10min_avg', 'ActivePower'),
               ('blade_angleA_DOW_2023_10min_avg', 'BladeAngleA'),
               ('RPM_DOW_2023_10min_avg', 'GenRPM'),
               ('windspeed_DOW_2023_10min_avg', 'WindSpeed'),
               ('wind_direction_DOW_2023_10min_avg', 'WindDirection'),
               ('yaw_angle_DOW_2023_10min_avg', 'NacelleDirection')]


def prepare_turbine_seperated_data(turbine_set = NAMES, include_ti = True): #unfiltered
    turbine_seperated_data = {}
    pres_hum = data['DOW_2023_Air_Pres_Hum']
    temp = data['DOW_2023_AirTemp']
    for code in turbine_set:
        turbine_data = pd.DataFrame()
        for file, dl in data_labels:
            temp_add = data[file][[f'DOW-{code}-{dl}', 'timestamp']]
            if len(turbine_data) == 0:  #If nothing to merge with
                turbine_data = temp_add
            else:
                turbine_data = pd.merge(turbine_data, temp_add, on='timestamp', how='outer')
            turbine_data = turbine_data.rename(columns={f'DOW-{code}-{dl}': dl})

        turbine_data = pd.merge(turbine_data, pres_hum, on='timestamp', how='outer')
        turbine_data = pd.merge(turbine_data, temp, on='timestamp', how='outer')
        
        turbine_data = timestamp_to_datetime_index(turbine_data)
        if include_ti:
            ti = timestamp_to_datetime_index(data['simulated_ti'][[f'DOW-{code}-TI', 'timestamp']])
            turbine_data = pd.merge(turbine_data, ti, on='timestamp', how='outer')
            turbine_data = turbine_data.rename(columns={f'DOW-{code}-TI': 'TI'})
  
        turbine_data = turbine_data.rename(columns={'BladeAngleA': 'Pitch', 'NacelleDirection': 'YawAngle', 'DOW-EFS-AirHumidity': 'AirHumidity','DOW-EFS-AirPres': 'AirPressure', 'DOW-EFS-AirTemp-2m' : 'AirTemp'})

        turbine_data['AirHumidity'] = turbine_data['AirHumidity'].ffill()       #because at hourly intervals
        turbine_data['AirPressure'] = turbine_data['AirPressure'].ffill()       #because at hourly intervals
        turbine_data['AirTemp'] = turbine_data['AirTemp'].ffill()       #because at hourly intervals

        turbine_data['TSR'] = (154 * np.pi * turbine_data['GenRPM']/60)/turbine_data['WindSpeed']
        turbine_data['YawOffset'] = turbine_data['WindDirection'] - turbine_data['YawAngle']

        turbine_data = turbine_data.dropna(how='any')  #only include full featuresets
        turbine_seperated_data[code] = turbine_data

    return turbine_seperated_data

def get_filtered_data(turbine_set=NAMES, include_ti = True):
    all_turbines_data = prepare_turbine_seperated_data(turbine_set, include_ti=include_ti)

    def _filter_by_masks(turbine_data):
        #To be excluded
        masks = ( #Easy to add more masks
            ((turbine_data['WindSpeed'] > 4) & (turbine_data['ActivePower'] < 10) & (turbine_data['WindSpeed'] < 25)) |
            (turbine_data['ActivePower'] < 0)
        )
        
        turbine_data = turbine_data[~masks]
        return turbine_data
    
    def _filter_by_quantiles(group):#removing outliers
        lower_quantile = group['ActivePower'].quantile(0.005) 
        upper_quantile = group['ActivePower'].quantile(0.995) 
        return group[(group['ActivePower'] >= lower_quantile) & (group['ActivePower'] <= upper_quantile)]

    for code, turbine_data in all_turbines_data.items():

        turbine_data = _filter_by_masks(turbine_data=turbine_data)

        turbine_data['WindSpeedBin'] = pd.cut(turbine_data['WindSpeed'], bins=100)
        turbine_data = turbine_data.groupby('WindSpeedBin', observed=False, group_keys=False).apply(lambda x: _filter_by_quantiles(x), include_groups=False).reset_index()
        
        all_turbines_data[code] = timestamp_to_datetime_index(turbine_data).sort_values('timestamp')
    return all_turbines_data


if __name__== '__main__':
    turbine_dataxx = prepare_turbine_seperated_data()
    filtered_data = get_filtered_data()

    turbine_dataxx['A01'].plot.scatter(x='WindSpeed', y='ActivePower', edgecolor='gray', alpha=0.6, title='A01 - Raw Measurements')
    #print(turbine_dataxx['A01'].nlargest(n=10, columns='YawOffset', keep='all'))
    #print(filtered_data['A01'].nlargest(n=10, columns='YawOffset', keep='all'))
    filtered_data['A01'].plot.scatter(x='WindSpeed', y='ActivePower',edgecolor='gray', alpha=0.6, title='A01 - Filtered Measurements')
    plt.show()

