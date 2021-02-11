#%%
import numpy as np
import matplotlib.pyplot as plt
i_teilnehmer = 3
lastprofilnummer = 3

Lastprofile_Mfh = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_MFH.npy', allow_pickle=True)
leistung_last_mfh = Lastprofile_Mfh[:, i_teilnehmer - 1]
Lastprofile_GW = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_Gewerbe.npy', allow_pickle=True)
leistung_last_gw = Lastprofile_GW[:,lastprofilnummer]

plt.plot(leistung_last_gw*1000)
# %%
