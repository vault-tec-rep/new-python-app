#%%
import scipy.io 
import numpy as np
# Wetterdaten
#%%
#GlobalStr
struct = scipy.io.loadmat('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_App\\Daten Wetter und Last\\Last_und_Wetter\\GlobalStr_Neu.mat')
GlobalStr = struct["GlobalStr_Neu"]
np.save('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\GlobalStr.npy', GlobalStr, allow_pickle=True)
#%%
#DiffusStr
struct = scipy.io.loadmat('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_App\\Daten Wetter und Last\\Last_und_Wetter\\DiffusStr_Neu.mat')
DiffusStr = struct["DiffusStr_Neu"]
np.save('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\DiffusStr.npy', DiffusStr, allow_pickle=True)
# %%
#TAMB
struct = scipy.io.loadmat('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_App\\Daten Wetter und Last\\Last_und_Wetter\\Air_Temp.mat')
tamb = struct["Air_Temp"]
np.save('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Air_temp.npy', tamb, allow_pickle=True)
#%%
Lastprofil_s = scipy.io.loadmat('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_App\\Daten Wetter und Last\\Last_und_Wetter\\Lastprofil_NUMPY.mat')
Lastprofil = Lastprofil_s["Lastprofil"]
np.save('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofil_ev.npy', Lastprofil, allow_pickle=True)
# %%
Wirkleistung_s = scipy.io.loadmat('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_App\\Daten Wetter und Last\\Last_und_Wetter\\Wirkleistung_Jahr_Sortiert_NUMPY.mat')
Wirkleistung_Jahr_Sortiert = Wirkleistung_s["Wirkleistung_Jahr_Sortiert"]
np.save('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Wirkleistung_Jahr_Sortiert.npy', Wirkleistung_Jahr_Sortiert, allow_pickle=True)
# %%
Index_Last_s = scipy.io.loadmat('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_App\\Daten Wetter und Last\\Last_und_Wetter\\Index_Last_NUMPY.mat')
Index_Last = Index_Last_s["Index_Last"]
np.save('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Index_Last.npy', Index_Last, allow_pickle=True)
# %%
Lastprofile_mfh_s = scipy.io.loadmat('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_App\\Daten Wetter und Last\\Last_und_Wetter\\Lastprofile_MFH.mat')
Lastprofile_MFH = Lastprofile_mfh_s["Lastprofile_Mfh"]
np.save('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_MFH.npy', Lastprofile_MFH, allow_pickle=True)
# %%
Lastprofile_gw_s = scipy.io.loadmat('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_App\\Daten Wetter und Last\\Last_und_Wetter\\Lastprofil_Gewerbe_NUMPY.mat')
Lastprofile_Gewerbe = Lastprofile_gw_s["Lastprofile_GW"]
np.save('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_Gewerbe.npy', Lastprofile_Gewerbe, allow_pickle=True)

# %%
