#%%
import numpy as np
import matplotlib.pyplot as plt
i_teilnehmer = 3
lastprofilnummer = 5

Lastprofile_Mfh = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_MFH.npy', allow_pickle=True)
leistung_last_mfh = Lastprofile_Mfh[:, i_teilnehmer - 1]
Lastprofile_GW = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_Gewerbe.npy', allow_pickle=True)
leistung_last_gw = Lastprofile_GW[:,lastprofilnummer]

leistung_1 = np.reshape(leistung_last_gw, (365, 96))
#plt.imshow(leistung_1, cmap='hot', interpolation='nearest')
durchschnittstag_last = leistung_1.sum(axis=0) / 365
plt.plot(durchschnittstag_last)
# %%
import numpy as np
a = np.array([1, 2, 3, 4, 5])
b = np.array([1, 1, 1, 1, 1])
# %%
