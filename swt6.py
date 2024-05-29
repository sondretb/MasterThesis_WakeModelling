from matplotlib import pyplot as plt
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.wind_turbines.generic_wind_turbines import GenericWindTurbine
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

power_list = np.array([
			['0', 0],['0.5', 0],['1', 0],['1.5', 0],['2', 0],['2.5', 0],['3', 0],['3.5', 100],['4', 220],['4.5', 320],['5', 440],['5.5', 575],['6', 721],['6.5', 945],['7', 1173],['7.5', 1485],['8', 1796],['8.5', 2157],['9', 2517],['9.5', 2940],['10', 3360],['10.5', 3930],['11', 4485],['11.5', 5160],['12', 5792],['12.5', 5960],['13', 6000],['13.5', 6000],['14', 6000],['14.5', 6000],['15', 6000],['15.5', 6000],['16', 6000],['16.5', 6000],['17', 6000],['17.5', 6000],['18', 6000],['18.5', 6000],['19', 6000],['19.5', 6000],['20', 6000],['20.5', 6000],['21', 6000],['21.5', 6000],['22', 6000],['22.5', 6000],['23', 6000],['23.5', 6000],['24', 6000],['24.5', 6000],['25', 6000],['25.5', 0],['26', 0],['26.5', 0],['27', 0],['27.5', 0],['28', 0],['28.5', 0],['29', 0],['29.5', 0],['30', 0],['30.5', 0],['31', 0],['31.5', 0],['32', 0],['32.5', 0],['33', 0],['33.5', 0],['34', 0],['34.5', 0],['35', 0]])

inspection_df = pd.DataFrame(power_list, columns=['u', 'power'])
inspection_df['u'] = inspection_df['u'].astype(float)

u = inspection_df['u'].to_numpy()
power = inspection_df['power'].to_numpy()
ct = np.full(len(power), 1)


POWER_CURVE_SWT6_external = PowerCtTabular(u, power, 'kw', ct)

SWT6 = GenericWindTurbine(name='SWT6.0-154', hub_height=110, diameter=154, power_norm=6000, ws_cutout=25)

def power_curve():
    pc = SWT6.power_ct()[0]


def plot_DOW_powercurve():
    X_Y_Spline = make_interp_spline(u[2:31], power[2:31])

    u_plot_cutin = np.linspace(0, 3.2, 100)
    u_plot_unrated = np.linspace(3.2, 13, 100)
    u_plot_rated = np.linspace(13, 25, 100)
    u_plot_cutout = np.linspace(25, 35, 100)


    power_plot_cutin = np.zeros(100)
    power_plot_cutout = np.zeros(100)
    
    power_plot_unrated = X_Y_Spline(u_plot_unrated)
    power_plot_rated = np.full(100, 6000)

    power_ = np.concatenate([power_plot_cutin, power_plot_unrated, power_plot_rated, power_plot_cutout])
    u_ = np.concatenate([u_plot_cutin, u_plot_unrated, u_plot_rated, u_plot_cutout])


    plt.plot(u_, power_, 'orange', linewidth = 2)

    plt.xlabel('Wind speed (m/s)')
    plt.ylabel('Power (kW)')
    plt.title('SWT-6.0 Power Curve')
    plt.grid()

if __name__ == "__main__":
    #plot_DOW_powercurve()
    SWT6.plot_power_ct()
    
    plt.show()
