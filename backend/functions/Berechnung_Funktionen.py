def berechnung_ev(Standort, kW, Jahresstromverbrauch, Strompreis, Azimuth,
                    Aufstellwinkel, KalkZins, Strompreissteigerung,
                    Speicher_kWh, Dachart, Aufstaenderung, Dachhaelften,
                    invest_parameter, betrieb_parameter, zusatzkosten, einspeiseverguetung_vektor, absolute_kosten):

    from Eigenverbrauch_Funktionen import oekonomie_vorbereiten_ev_speicher, \
        oekonomie_berechnen_ev_speicher, last_waehlen
    from Allgemeine_Funktionen import wetter_waehlen, pv_werte_waehlen, berechnung_pv_vektor
    import numpy as np
    import pandas as pd

    air_temp = np.load('Ausgangsdaten/Air_temp.npy', allow_pickle=True)
    GlobalStr = np.load('Ausgangsdaten/GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('Ausgangsdaten/DiffusStr.npy', allow_pickle=True)
    Lastprofil = np.load('Ausgangsdaten/Lastprofil_ev.npy', allow_pickle=True)
    Wirkleistung_Jahr_Sortiert = np.load('Ausgangsdaten/Wirkleistung_Jahr_Sortiert.npy', allow_pickle=True)
    IndexLast = np.load('Ausgangsdaten/Index_Last.npy', allow_pickle=True)
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')

    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Aufstaenderung, Dachhaelften)
    eco = oekonomie_vorbereiten_ev_speicher(Strompreis, kW, Strompreissteigerung, Speicher_kWh, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten)
    lastprofil_wahl = last_waehlen(Jahresstromverbrauch, Lastprofil, Wirkleistung_Jahr_Sortiert, IndexLast)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_ev_speicher(leistung_pv, lastprofil_wahl, eco, kW, KalkZins, Speicher_kWh, einspeiseverguetung_vektor)

    return barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten


def berechnung_ms(Standort, Dachart, Aufstaenderung, Dachhaelften, Strompreis, kW, Strompreissteigerung, 
                    i_teilnehmer, Azimuth, Aufstellwinkel, mieterstromzuschlag, KalkZins, betreiber,
                    invest_parameter, betrieb_parameter, zusatzkosten, einspeiseverguetung_vektor, absolute_kosten):
    from Mehrfamilienhaus_Funktionen import oekonomie_vorbereiten_ms, \
        oekonomie_berechnen_ms
    from Allgemeine_Funktionen import wetter_waehlen, pv_werte_waehlen, berechnung_pv_vektor
    import numpy as np
    import pandas as pd

    air_temp = np.load('Ausgangsdaten/Air_temp.npy', allow_pickle=True)
    GlobalStr = np.load('Ausgangsdaten/GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('Ausgangsdaten/DiffusStr.npy', allow_pickle=True)
    Lastprofile_Mfh = np.load('Ausgangsdaten/Lastprofile_MFH.npy', allow_pickle=True)
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    Lastprofil_MS = Lastprofile_Mfh[:, i_teilnehmer - 1]


    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Aufstaenderung, Dachhaelften)
    eco = oekonomie_vorbereiten_ms(Strompreis, kW, Strompreissteigerung, i_teilnehmer, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_ms(leistung_pv, Lastprofil_MS, eco, kW, mieterstromzuschlag, KalkZins, betreiber, einspeiseverguetung_vektor)
    
    return barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten


def berechnung_gw_ev(Standort, Dachart, Aufstaenderung, Dachhaelften, 
                     Strompreis, kW, Strompreissteigerung, Azimuth, Aufstellwinkel, KalkZins, Jahresstromverbrauch, Lastprofil_Nummer,
                     invest_parameter, betrieb_parameter, zusatzkosten, einspeiseverguetung_vektor, eigenverbrauchsanteil, lastprofil_verwenden, absolute_kosten):
    from Gewerbe_Funktionen import oekonomie_vorbereiten_gw, \
        oekonomie_berechnen_gw_ev
    from Allgemeine_Funktionen import wetter_waehlen, pv_werte_waehlen, berechnung_pv_vektor
    import numpy as np
    import pandas as pd

    air_temp = np.load('Ausgangsdaten/Air_temp.npy', allow_pickle=True)
    GlobalStr = np.load('Ausgangsdaten/GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('Ausgangsdaten/DiffusStr.npy', allow_pickle=True)
    Lastprofile_GW = np.load('Ausgangsdaten/Lastprofile_Gewerbe.npy', allow_pickle=True)
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    lastprofil_wahl = Lastprofile_GW[:,Lastprofil_Nummer]

    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Aufstaenderung, Dachhaelften)
    eco = oekonomie_vorbereiten_gw(Strompreis, kW, Strompreissteigerung, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_gw_ev(leistung_pv, lastprofil_wahl, eco, kW, KalkZins,
     Jahresstromverbrauch, einspeiseverguetung_vektor, eigenverbrauchsanteil, lastprofil_verwenden)

    return barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten

def berechnung_gw_ds(Standort, Dachart, Aufstaenderung, Dachhaelften, Strompreis,
                        kW, Strompreissteigerung, Azimuth, Aufstellwinkel, KalkZins, Jahresstromverbrauch, Betreiber, Lastprofil_Nummer,
                        invest_parameter, betrieb_parameter, zusatzkosten, einspeiseverguetung_vektor, eigenverbrauchsanteil, lastprofil_verwenden, absolute_kosten):
    
    from Gewerbe_Funktionen import oekonomie_vorbereiten_gw_ds, \
        oekonomie_berechnen_gw_ds
    from Allgemeine_Funktionen import wetter_waehlen, pv_werte_waehlen, berechnung_pv_vektor
    import numpy as np
    import pandas as pd
    
    air_temp = np.load('Ausgangsdaten/Air_temp.npy', allow_pickle=True)
    GlobalStr = np.load('Ausgangsdaten/GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('Ausgangsdaten/DiffusStr.npy', allow_pickle=True)
    Lastprofile_GW = np.load('Ausgangsdaten/Lastprofile_Gewerbe.npy', allow_pickle=True)
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    lastprofil_wahl = Lastprofile_GW[:, Lastprofil_Nummer]

    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Aufstaenderung, Dachhaelften)
    eco = oekonomie_vorbereiten_gw_ds(Strompreis, kW, Strompreissteigerung, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_gw_ds(leistung_pv, lastprofil_wahl, eco, kW, KalkZins, Betreiber,
     Jahresstromverbrauch, einspeiseverguetung_vektor, eigenverbrauchsanteil, lastprofil_verwenden)
    
    return barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten

def berechnung_gw_ve(Standort, Dachart, Aufstaenderung, Dachhaelften, kW, Azimuth, Aufstellwinkel, KalkZins,
                        invest_parameter, betrieb_parameter, zusatzkosten, einspeiseverguetung_vektor, absolute_kosten):
    from Gewerbe_Funktionen import oekonomie_vorbereiten_gw_ve, \
        oekonomie_berechnen_gw_ve
    from Allgemeine_Funktionen import wetter_waehlen, pv_werte_waehlen, berechnung_pv_vektor
    import numpy as np
    import pandas as pd
    
    air_temp = np.load('Ausgangsdaten/Air_temp.npy', allow_pickle=True)
    GlobalStr = np.load('Ausgangsdaten/GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('Ausgangsdaten/DiffusStr.npy', allow_pickle=True)
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')

    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(Standort, air_temp, GlobalStr, DiffusStr)
    logisch_doppelte_rechnung = pv_werte_waehlen(Dachart, Aufstaenderung, Dachhaelften)
    eco = oekonomie_vorbereiten_gw_ve(kW, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, Azimuth, Aufstellwinkel, kW, logisch_doppelte_rechnung)
    [barwert, rendite, gewinnkurve, stromgestehungskosten] = oekonomie_berechnen_gw_ve(leistung_pv, eco, kW, KalkZins, einspeiseverguetung_vektor)

    return barwert, rendite, gewinnkurve, stromgestehungskosten