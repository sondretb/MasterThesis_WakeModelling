from py_wake.literature.gaussian_models import Bastankhah_PorteAgel_2014
from py_wake.literature.noj import Jensen_1983
from py_wake.superposition_models import LinearSum, SquaredSum
from py_wake.examples.data.iea37._iea37 import IEA37Site
import pandas as pd
from util import ws2ti_0

from swt6 import SWT6
from dudgeon import NAMES, WT_X, WT_Y

class WakeEstimator:
    def __init__(self, deficitModel, superpositionModel, k):
        self.wfm = deficitModel(site=IEA37Site(), windTurbines=SWT6, superpositionModel=superpositionModel(), k=k)

    def predict(self, X):
        sim_results = self.wfm(x=WT_X, y=WT_Y, ws=X[0], wd=X[1])
        return sim_results.to_dataframe()['WS_eff'].to_list()
    

class WakeEstimatorTI:
    def __init__(self, superpositionModel):
        self.superpositionModel = superpositionModel

    def _get_k(self, ws):
        ti = ws2ti_0(ws)
        if ti> 0.065 and ti< 0.15:
            k = 0.3837 * ti + 0.03678
        else: k = 0.3837 * 0.09 + 0.03678 #set 0.09 as ti default
        return k
    
    def predict(self, X):
        wfm = Bastankhah_PorteAgel_2014(site=IEA37Site(), superpositionModel=self.superpositionModel(), k=self._get_k(X[0]), windTurbines=SWT6)
        sim_results = wfm(x=WT_X, y=WT_Y, ws=X[0], wd=X[1])
        return sim_results.to_dataframe()['WS_eff'].to_list()
    
if __name__ == '__main__':
    we = WakeEstimator(Jensen_1983, LinearSum, 0.05)
    print(we.predict([10, 270]))
