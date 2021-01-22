# Imports
from Eigenverbrauch_Funktionen import oekonomie_vorbereiten_ev_speicher, \
    oekonomie_berechnen_ev_speicher, last_waehlen
from Mehrfamilienhaus_Funktionen import oekonomie_vorbereiten_ms, \
    oekonomie_berechnen_ms
from Gewerbe_Funktionen import oekonomie_vorbereiten_gw, \
    oekonomie_berechnen_gw_ev, oekonomie_vorbereiten_gw_ds, oekonomie_berechnen_gw_ds,\
    oekonomie_vorbereiten_gw_ve, oekonomie_berechnen_gw_ve
from Allgemeine_Funktionen import wetter_waehlen, pv_werte_waehlen, berechnung_pv_vektor

import numpy as np
import pandas as pd
#from timeit import default_timer as timer

# Festlegung des zu testenden Geschäftsmodells
# 1 = Eigenverbrauch, 2 = Mieterstrom, 3 = Gewerbe Eigenverbrauch,
# 4 = Gewerbe Direktstromlieferung, 5 = Gewerbe Volleinspeisung
geschaeftsmodell = 1

if geschaeftsmodell == 1:
    #Laden der Daten
    air_temp = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Air_Temp.npy', allow_pickle=True)
    GlobalStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\DiffusStr.npy', allow_pickle=True)
    Lastprofil = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofil_ev.npy', allow_pickle=True)
    Wirkleistung_Jahr_Sortiert = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Wirkleistung_Jahr_Sortiert.npy', allow_pickle=True)
    IndexLast = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Index_Last.npy', allow_pickle=True)
    
    # Eingangsparameter
    Standort = '1'
    zeit_vektor = pd.date_range('2010-01-01 00:00:00',
                                '2010-12-31 23:59:00', freq='1min')
    kW = 10
    Jahresstromverbrauch = 3000
    Strompreis = 28
    Azimuth = 180
    Aufstellwinkel = 15
    KalkZins = 2
    Strompreissteigerung = 2
    Speicher_kWh = 5
    Dachart = '2'  # 1 = Flachdach, 2 = Schraegdach
    WelchesDach = '1'  # 1 = Eine Hälfte, 2 = Beide Hälften
    Dachkonfiguration = '2'  # 1 = Trapez, 2 = Hintereinander
    invest_parameter = [1923, -0.16]
    betrieb_parameter = [148, 5]
    zusatzkosten = 0
    einspeiseverguetung_vektor = [9.30, 9.05, 7.19]

    #Berechnung
    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Dachkonfiguration, WelchesDach)
    eco = oekonomie_vorbereiten_ev_speicher(Strompreis, kW, Strompreissteigerung, Speicher_kWh, invest_parameter, betrieb_parameter, zusatzkosten)
    lastprofil_wahl = last_waehlen(Jahresstromverbrauch, Lastprofil, Wirkleistung_Jahr_Sortiert, IndexLast)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_ev_speicher(leistung_pv, lastprofil_wahl, eco, kW, KalkZins, Speicher_kWh, einspeiseverguetung_vektor)
    print("Barwert: ", barwert)
    print("Rendite: ", rendite)
    print("Eigenverbrauchsanteil: ", eigenverbrauchsanteil)
    print("Autarkiegrad: ", autarkiegrad)
    print("Stromgestehungskosten: ", stromgestehungskosten)
elif geschaeftsmodell == 2:
    #Laden der Daten
    air_temp = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Air_Temp.npy', allow_pickle=True)
    GlobalStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\DiffusStr.npy', allow_pickle=True)
    Lastprofile_Mfh = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_MFH.npy', allow_pickle=True)
    
    # Eingangsparameter
    Standort = '1'
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    kW = 20
    Strompreis = 28
    Azimtuh = 0
    Aufstellwinkel = 15
    KalkZins = 2
    Strompreissteigerung = 2
    i_teilnehmer = 5
    betreiber = 'Betreiber'
    Dachart = 2 # 1 = Flachdach, 2 = Schraegdach
    WelchesDach = 1 #  1 = Eine Hälfte, 2 = Beide Hälften
    Dachkonfiguration = 2 # 1 = Trapez, 2 = Hintereinander
    Lastprofil_MS = Lastprofile_Mfh[:,i_teilnehmer - 1]
    mieterstromzuschlag = 'Nein'
    invest_parameter = [1923, -0.16]
    betrieb_parameter = [148, 5]
    zusatzkosten = 0
    einspeiseverguetung_vektor = [9.30, 9.05, 7.19]

    #Berechnung
    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Dachkonfiguration, WelchesDach)
    eco = oekonomie_vorbereiten_ms(Strompreis, kW, Strompreissteigerung, i_teilnehmer, invest_parameter, betrieb_parameter, zusatzkosten)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimtuh, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_ms(leistung_pv, Lastprofil_MS, eco, kW, mieterstromzuschlag, KalkZins, betreiber, einspeiseverguetung_vektor)
    print("Barwert: ", barwert)
    print("Rendite: ", rendite)
    print("Eigenverbrauchsanteil: ", eigenverbrauchsanteil)
    print("Autarkiegrad: ", autarkiegrad)
    print("Stromgestehungskosten: ", stromgestehungskosten)
elif geschaeftsmodell == 3:
    #Laden der Daten
    air_temp = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Air_Temp.npy', allow_pickle=True)
    GlobalStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\DiffusStr.npy', allow_pickle=True)
    Lastprofile_GW = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_Gewerbe.npy', allow_pickle=True)
    
    #Eingangsparameter
    Standort = '1'
    kW = 30
    Jahresstromverbrauch = 35000
    Strompreis = 18
    Azimuth = 0
    Aufstellwinkel = 15
    KalkZins = 2
    Strompreissteigerung = 2
    Dachart = 2 # 1 = Flachdach, 2 = Schraegdach
    WelchesDach = 1 #  1 = Eine Hälfte, 2 = Beide Hälften
    Dachkonfiguration = 2 # 1 = Trapez, 2 = Hintereinander
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    lastprofil_wahl = Lastprofile_GW[:,0]
    invest_parameter = [1923, -0.16]
    betrieb_parameter = [148, 5]
    zusatzkosten = 0
    einspeiseverguetung_vektor = [9.30, 9.05, 7.19]
    eigenverbrauchsanteil = 0
    lastprofil_verwenden = True

    #Berechnung
    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Dachkonfiguration, WelchesDach)
    eco = oekonomie_vorbereiten_gw(Strompreis, kW, Strompreissteigerung, invest_parameter, betrieb_parameter, zusatzkosten)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_gw_ev(leistung_pv, lastprofil_wahl, eco, kW, KalkZins, Jahresstromverbrauch, einspeiseverguetung_vektor, eigenverbrauchsanteil, lastprofil_verwenden)
    print("Barwert: ", barwert)
    print("Rendite: ", rendite)
    print("Eigenverbrauchsanteil: ", eigenverbrauchsanteil)
    print("Autarkiegrad: ", autarkiegrad)
    print("Stromgestehungskosten: ", stromgestehungskosten)
elif geschaeftsmodell == 4:
    #Ladend der Daten
    air_temp = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Air_Temp.npy', allow_pickle=True)
    GlobalStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\DiffusStr.npy', allow_pickle=True)
    Lastprofile_GW = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_Gewerbe.npy', allow_pickle=True)

    #Eingangsparameter
    Standort = '1'
    kW = 30
    Jahresstromverbrauch = 35000
    Strompreis = 18
    Azimuth = 0
    Aufstellwinkel = 15
    KalkZins = 2
    Strompreissteigerung = 2
    Dachart = 2 # 1 = Flachdach, 2 = Schraegdach
    WelchesDach = 1 #  1 = Eine Hälfte, 2 = Beide Hälften
    Dachkonfiguration = 2 # 1 = Trapez, 2 = Hintereinander
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    lastprofil_wahl = Lastprofile_GW[:,0]
    Betreiber = 'betreiber-0'
    invest_parameter = [1923, -0.16]
    betrieb_parameter = [148, 5]
    zusatzkosten = 0
    einspeiseverguetung_vektor = [9.30, 9.05, 7.19]
    eigenverbrauchsanteil = 0
    lastprofil_verwenden = True

    #Berechnung
    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Dachkonfiguration, WelchesDach)
    eco = oekonomie_vorbereiten_gw_ds(Strompreis, kW, Strompreissteigerung, invest_parameter, betrieb_parameter, zusatzkosten)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_gw_ds(leistung_pv, lastprofil_wahl, eco, kW, KalkZins, Betreiber, Jahresstromverbrauch, einspeiseverguetung_vektor, eigenverbrauchsanteil, lastprofil_verwenden)
    print("Barwert: ", barwert)
    print("Rendite: ", rendite)
    print("Eigenverbrauchsanteil: ", eigenverbrauchsanteil)
    print("Autarkiegrad: ", autarkiegrad)
    print("Stromgestehungskosten: ", stromgestehungskosten)
elif geschaeftsmodell == 5:
    #Laden der Daten
    air_temp = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Air_Temp.npy', allow_pickle=True)
    GlobalStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\DiffusStr.npy', allow_pickle=True)
    
    #Eingangsparameter
    Standort = '1'
    kW = 30
    Jahresstromverbrauch = 35000
    Strompreis = 18
    Azimuth = 0
    Aufstellwinkel = 15
    KalkZins = 2
    Strompreissteigerung = 2
    Dachart = 2 # 1 = Flachdach, 2 = Schraegdach
    WelchesDach = 1 #  1 = Eine Hälfte, 2 = Beide Hälften
    Dachkonfiguration = 2 # 1 = Trapez, 2 = Hintereinander
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    invest_parameter = [1923, -0.16]
    betrieb_parameter = [148, 5]
    zusatzkosten = 0
    einspeiseverguetung_vektor = [9.30, 9.05, 7.19]


    #Berechnung
    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Dachkonfiguration, WelchesDach)
    eco = oekonomie_vorbereiten_gw_ve(kW, invest_parameter, betrieb_parameter, zusatzkosten)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, stromgestehungskosten] = oekonomie_berechnen_gw_ve(leistung_pv, eco, kW, KalkZins, einspeiseverguetung_vektor)
    print("Barwert: ", barwert)
    print("Rendite: ", rendite)
    print("Stromgestehungskosten: ", stromgestehungskosten)
else:
    print("Sollte nicht passieren. Geschäftsmodell Definition überprüfen")
