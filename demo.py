from py_wake.literature.noj import Jensen_1983
from py_wake import BastankhahGaussian
from py_wake.literature.gaussian_models import Bastankhah_PorteAgel_2014
from py_wake.turbulence_models import STF2017TurbulenceModel, GCLTurbulence, STF2005TurbulenceModel
from py_wake.utils.plotting import setup_plot
from py_wake.deflection_models import JimenezWakeDeflection, DeflectionModel
from py_wake.turbulence_models import TurbulenceModel
from py_wake.deficit_models.deficit_model import DeficitModel
from py_wake.site import UniformSite
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from py_wake.examples.data.iea37._iea37 import IEA37Site
from py_wake.examples.data.hornsrev1 import V80
from py_wake.wind_turbines import WindTurbines
import pandas as pd
from dudgeon import WT_X, WT_Y, NAMES
from typing import List
import numpy as np



def plot_flowmap_demo(deficit_model: DeficitModel, deflection_model: DeflectionModel, turbulence_model: TurbulenceModel, yaw=None, ws=10, wd=270, ti = 0):
    if yaw:
        turbine_amount = len(yaw)
        wt_x = [1000*i for i in range(turbine_amount)]
        wt_y = [0*i for i in range(turbine_amount)]
    else:
        yaw=[0]

    if not turbulence_model:
        plot_turbulence = False
        print("can't plot turbulence, no model specified")
    else:
        turbulenceModel = turbulence_model()
        plot_turbulence = True


    windTurbines = V80()
    site = IEA37Site(ti=ti)
    D = windTurbines.diameter()

    wfm = deficit_model(site=site, windTurbines=windTurbines, deflectionModel=deflection_model(), turbulenceModel = turbulenceModel)


    sim_results = wfm(x=wt_x, y=wt_y, ws=ws, wd=wd, yaw=yaw, tilt=0)


    flow_map = sim_results.flow_map()
    print(sim_results.to_dataframe())
    

    # Plot wake map
    plt.figure(wfm.__class__.__name__, figsize=(4*turbine_amount, 4))
    plt.title("Wake deficit model: " + wfm.__class__.__name__)


    flow_map.plot_wake_map(normalize_with=D)

    if plot_turbulence:
        plt.figure(turbulenceModel.__class__.__name__, figsize=(4*turbine_amount, 4))
        plt.title("Turbulence Model: " + turbulenceModel.__class__.__name__)
        flow_map.plot(flow_map.TI_eff, clabel="Added turbulence intensity [-]", levels=100, cmap="Blues", normalize_with=D)

    plt.show()

def plot_DOW(deficit_model: DeficitModel, deflection_model: DeflectionModel, turbulence_model: TurbulenceModel, yaw=[0 for _ in range(len(WT_Y))], ws=10, wd=270):
    turbine_amount = len(WT_Y)
    
    if len(yaw) != turbine_amount:
        raise Exception(f"Yaw list not of dimention {turbine_amount}.")
    
    if not turbulence_model:
        plot_turbulence = False
        print("can't plot turbulence, no model specified")
    else:
        turbulenceModel = turbulence_model()
        plot_turbulence = True

    windTurbines = V80()
    dow_windturbines = WindTurbines(names=NAMES, diameters=[154 for _ in range(len(NAMES))], hub_heights=[110 for _ in range(len(NAMES))], powerCtFunctions=[windTurbines.powerCtFunction]*len(NAMES))

    site = IEA37Site()
    D = windTurbines.diameter()

    wfm = deficit_model(site=site, windTurbines=windTurbines, deflectionModel=deflection_model(), turbulenceModel = turbulenceModel)

    sim_results = wfm(x=WT_X, y=WT_Y, ws=ws, wd=wd, yaw=yaw, tilt=0)


    flow_map = sim_results.flow_map()
    print(sim_results.to_dataframe())
    
    # Plot wake map
    plt.figure(wfm.__class__.__name__, figsize=(4, 4))
    plt.title("Wake deficit model: " + wfm.__class__.__name__)


    flow_map.plot_wake_map(normalize_with=D)
    

    if plot_turbulence:
        plt.figure(turbulenceModel.__class__.__name__, figsize=(4, 4))
        plt.title("Turbulence Model: " + turbulenceModel.__class__.__name__)
        flow_map.plot(flow_map.TI_eff, clabel="Added turbulence intensity [-]", levels=100, cmap="Blues", normalize_with=D)

    plt.show()



def plot_DOW_layout(highlight: List[str] | str = [], color ='b', highlight_color = 'r'):
    ax = plt.gca()
    r = int(154/2)

    for name, x, y in zip(NAMES, WT_X, WT_Y):
        marker = 'o'+color
        if name in highlight:
            marker = 'o'+highlight_color
        ax.annotate(name, (x+r*1.3, y+r*1.5), fontsize=7)
        plt.plot(x, y, marker)
    plt.title('DOW Layout')
    
    plt.show()





if __name__ == '__main__':
    """
    plot_DOW(deficit_model=BastankhahGaussian, 
                  deflection_model=JimenezWakeDeflection, 
                  turbulence_model=STF2017TurbulenceModel,
                  wd=290, ws=10, yaw=[0,0,0]+[ 0 for _ in range(len(WT_Y)-3)])
                  """
    
    #plot_DOW_layout()
    plot_flowmap_demo(deficit_model=Jensen_1983, 
                  deflection_model=JimenezWakeDeflection, 
                  turbulence_model=STF2017TurbulenceModel,
                  ti=0.05, yaw=[0, 0], wd=270)  



    

