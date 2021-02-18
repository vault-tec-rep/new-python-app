#%%
import numpy as np
kW = 30
jahresstromverbrauch = 30000
a =  np.round(0.3 * ((kW/(jahresstromverbrauch/1000))**(-0.55)), 1)
print(a)
# %%
