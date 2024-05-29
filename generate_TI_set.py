from dudgeon import WT_X, WT_Y, NAMES
from swt6 import SWT6
from py_wake.turbulence_models import STF2017TurbulenceModel
from py_wake.wind_farm_models.engineering_models import PropagateDownwind 
from py_wake.deficit_models.no_wake import NoWakeDeficit
from data_filter import get_filtered_data
import pandas as pd
import numpy as np
from util import ws2ti_0, timestamp_to_datetime_index
import time
from tqdm import tqdm
from py_wake.examples.data.iea37._iea37 import IEA37Site
import matplotlib.pyplot as plt

params_filename = './temp/simulation_entry_params.csv'
ti_filename = './data/simulated_ti.csv'

def _save_to_file():
    data = get_filtered_data(turbine_set=['A05'], include_ti=False)['A05']
    ws = data['WindSpeed'].to_numpy()
    data['TI_0'] = ws2ti_0(ws)
    data.to_csv(params_filename)

def _read_file():
    data = pd.read_csv(params_filename)
    return timestamp_to_datetime_index(data)

def _get_site(ti_0):
    site = IEA37Site(ti=ti_0)
    return site

def _get_column_list():
    return [f'DOW-{name}-TI' for name in NAMES]


def create_simulated_ti_set(ws, wd, ti_0, ts):
    ti_list = []
    for ws_i, wd_i, ti_0_i in tqdm(zip(ws, wd, ti_0), total=len(ws), desc='Generating turbulence intensity data set'):
        site = _get_site(ti_0 = ti_0_i)
        wfm = PropagateDownwind(site=site, wake_deficitModel=NoWakeDeficit(), turbulenceModel=STF2017TurbulenceModel(), windTurbines=SWT6)
        sim_results = wfm(x=WT_X, y=WT_Y, ws=ws_i, wd=wd_i)
        ti_list.append(sim_results.to_dataframe()['TI_eff'].to_list())

    ti_df = pd.DataFrame(data=ti_list, columns=_get_column_list(), index=ts)
    ti_df.index.name = 'timestamp'
    ti_df.to_csv(ti_filename)


if __name__ == '__main__':
    #_save_to_file()
    param_df = _read_file()
    ws = param_df['WindSpeed'].to_numpy()
    wd = param_df['WindDirection'].to_numpy()
    ti_0 = param_df['TI_0'].to_numpy()
    ts = param_df.index.to_numpy()
    create_simulated_ti_set(ws, wd, ti_0, ts)




