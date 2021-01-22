#Berechnungsfunktionen der Geschäftsmodelle. Die Funktionen greifen auf weiter unten definierte Funktionen zurück. 
def berechnung(strompreis, kW, strompreissteigerung, kalkZins, jahresstromverbrauch, lastprofilNummer,
                einspeiseverguetungVektor, i_teilnehmer, mieterstromzuschlag, spez_kosten_pv, geschäftsmodell):
    import numpy as np
    import pandas as pd

    air_temp = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Air_Temp.npy', allow_pickle=True)
    GlobalStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\DiffusStr.npy', allow_pickle=True)
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(air_temp, GlobalStr, DiffusStr)
    eco = oekonomie_vorbereiten(strompreis, kW, strompreissteigerung, i_teilnehmer,spez_kosten_pv, geschäftsmodell)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, kW)
    
    if geschäftsmodell == 1: # Mieterstrom
        Lastprofile_Mfh = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_MFH.npy', allow_pickle=True)
        Lastprofil_MS = Lastprofile_Mfh[:, i_teilnehmer - 1]

        [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_ms(leistung_pv, Lastprofil_MS, eco, kW, mieterstromzuschlag, kalkZins, betreiber, einspeiseverguetungVektor)
        return barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten

    elif geschäftsmodell == 2: # Gewerbe oder NWG
        Lastprofile_GW = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_Gewerbe.npy', allow_pickle=True)
        lastprofil_wahl = Lastprofile_GW[:,lastprofilNummer]

        [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = oekonomie_berechnen_gw_ev(leistung_pv, lastprofil_wahl, eco, kW, kalkZins,
        jahresstromverbrauch, einspeiseverguetungVektor, eigenverbrauchsanteil, lastprofil_verwenden)
        return barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten
    else:
         raise Exception('Fehler in Berechnungsfunktion. Geschäftsmodell falsch übergeben.')


#Allgemeine Funktionen, die von jedem Geschäftsmodell gebraucht werden
def poa(beam_horizontal, sky_diffuse_horizontal, zeit_vektor, azimuth_pv, tilt,
        latitude, longitude):
    # Import der Module
    import pvlib
    import numpy as np
    import math
    from timeit import default_timer as timer
    from ephemeris import ephemeris
    import copy
    import pandas as pd
    # Bestimmen der Sonnenpostition
    solpos = ephemeris(zeit_vektor, latitude, longitude)
  
    # Bestimmen des Einfallswinkels
    theta = pvlib.irradiance.aoi(
        tilt, azimuth_pv, solpos.zenith, solpos.azimuth)
    theta_numpy = theta.to_numpy()  # pylint: disable=maybe-no-member

    iam = np.maximum(0, 1 - 0.05 * (1 / np.cos(np.radians(np.minimum(90,theta_numpy))) -1))
    # Direkte Strahlung auf geneigter Ebene
    i = np.bitwise_and(solpos.elevation <= 2, beam_horizontal > 0)
    beam_horizontal[i] = 0

    elevation_numpy = solpos.elevation.to_numpy()

    g_direkt =  iam * beam_horizontal * np.cos(np.radians(theta_numpy)) / np.sin(np.radians(elevation_numpy))
    g_direkt[g_direkt < 0] = 0
    # Diffuse Strahlung nach Klucher
    global_irradiance = beam_horizontal + sky_diffuse_horizontal
    g_diffus_pv = pvlib.irradiance.klucher(tilt, azimuth_pv, sky_diffuse_horizontal, global_irradiance,
                                           solpos.elevation, solpos.azimuth)
    g_diffus_pv_numpy = g_diffus_pv.to_numpy()
    # Bodenreflexion
    g_reflexion = global_irradiance * 0.1 * (1 - np.cos(np.radians(tilt)))
    # Globalstrahlung PV
    g_global_pv = g_direkt + g_diffus_pv_numpy + g_reflexion
    g_global_pv[g_global_pv < 0] = 0
    return g_global_pv

def pv_syst(global_pv, air_temp, p_modul=300):
    import pvlib
    import pandas as pd
    cell_temp = pvlib.temperature.pvsyst_cell(global_pv, air_temp)
    p_pv_dc = pvlib.pvsystem.pvwatts_dc(global_pv, cell_temp, p_modul, -0.005)
    p_pv_ac = pvlib.pvsystem.pvwatts_ac(p_pv_dc, 1000) #Bald pvlib.inverter.ovwatts(p_pv_dc, 1000) !Deprecation!
    x_p_pv = (p_pv_ac / p_modul)  # P_AC / P_Nenn in Watt
    return x_p_pv

def wetter_waehlen(tamb, global_str, dhi):
    dirh = global_str - dhi # Berechnen der direkten Einstrahlung aus den Messwerten
    #Festlegen der Koordinaten
    breite = 52.388 
    laenge = 13.065
    #Extrahieren der richtigen Wetterdaten aus allen Wetterdaten
    dhi_extracted = dhi[:, 14]
    dirh_extracted = dirh[:, 14]
    tamb_extracted = tamb[:, 14]

    return dirh_extracted, dhi_extracted, tamb_extracted, breite, laenge

def berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, kW):
    import numpy as np
    import copy
    from Allgemeine_Funktionen import poa, pv_syst

    azimuth = 90
    aufstellwinkel = 15
    logisch_doppelte_rechnung = 1
    
    if logisch_doppelte_rechnung == 0:
        # Einstrahlung
        ghi_generatorebene = poa(
            dirh, dhi, zeit_vektor, azimuth, aufstellwinkel, breite, laenge)
        # Leistungsvektor
        prozent_leistung_pv = pv_syst(ghi_generatorebene, tamb)
        leistung_pv_gesamt = prozent_leistung_pv*kW*1000  # kW zu Watt
    else:
        azimuth_2 = azimuth + 180
        if azimuth_2 > 360:
            azimuth_2 -= 360
        n = -1
        azimuth_vektor = [azimuth, azimuth_2]

        for azimuth_loop in azimuth_vektor:
            n = n+1
            ghi_generatorebene = poa(
                dirh, dhi, zeit_vektor, azimuth_loop, aufstellwinkel, breite, laenge)
            prozent_leistung_pv = pv_syst(ghi_generatorebene, tamb)
            leistung_pv = prozent_leistung_pv*(kW/2)*1000  # kW zu Watt

            if n == 0:
                leistung_pv_1 = copy.deepcopy(leistung_pv)
        leistung_pv_gesamt = leistung_pv_1 + leistung_pv
    leistung_pv_gesamt[leistung_pv_gesamt < 0] = 0
    return leistung_pv_gesamt


#Unterfunktionen, die von den oberen beiden Berechnungsfunktionen aufgerufen werden
def oekonomie_vorbereiten(strompreis, kW, strompreissteigerung, i_teilnehmer,spez_kosten_pv, geschäftsmodell):
    # Imports
    import numpy as np

    # Berechnung
    strompreis /= 100  # Angabe als netto
    strompreissteigerung /= 100
    strompreis_vektor = np.zeros(20)
    eco = {}
    for zahl in range(20):
        if zahl > 0:
            strompreis *= (1 + strompreissteigerung)
        strompreis_vektor[zahl] = strompreis

    # EEG Umlage 2020 - 2035 nach Agora Energiewende vom. 17.08.2020, danach konstant angenommen
    eco["umlage"] = np.array([0.06756, 0.06919, 0.06591, 0.06416, 0.06348, 0.06163, 0.05799, 0.05326, 0.04982, 0.04591,
                              0.04106, 0.03362, 0.02654, 0.0234, 0.02110, 0.02110, 0.02110, 0.02110, 0.02110, 0.02110])
    eco["strompreis_vektor"] = strompreis_vektor

    # Investkosten
    invest_pv = spez_kosten_pv*kW  # netto, also ohne: *1.19 oder?

    if geschäftsmodell == 1: #Mieterstrom
        # Betriebskosten Mieterstrom nach Kelm2019:
        # c_Betrieb_jaehrl = 17 * kW  # 17 real 
        c_grundpreis = 100  # Quelle Kelm19 sagt: 50-100
        # c_messstelle = 100
        eco["grundpreis"] = c_grundpreis
        eco["i_teilnehmer"] = i_teilnehmer

        # Berni neu:
        c_messsystem_einmal_Kelm19 = 125 * i_teilnehmer # einmalig: Einmalige Investitionsausgaben für die Umsetzung des Messkonzepts in Höhe von 100 bis 150 Euro pro Teilnehmer
        c_messsystem_jaehrlich_Kelm19 = 75 * i_teilnehmer # jährlich: Kosten für Messstellenbetrieb, Abrechnung, Rechnungstellung und Vertrieb in Höhe von 50 bis 100 Euro pro Teilnehmer und Jahr
        
        eco["betrieb"] = 17*kW + c_messsystem_jaehrlich_Kelm19

        if kW >= 30: 
            eco["invest"] = np.round(invest_pv + c_messsystem_einmal_Kelm19, 2) + 3000
        else: 
            eco["invest"] = np.round(invest_pv + c_messsystem_einmal_Kelm19, 2)
    elif geschäftsmodell == 2:
        #betrieb
        if kW > 8:
            eco["betrieb"] = 145 + 5*kW + 21
        else: 
            eco["betrieb"] = 145 + 5*kW

        #invest
        if kW >= 30: 
            eco["invest"] = np.round(invest_pv, 2) + 3000
        else: 
            eco["invest"] = np.round(invest_pv, 2)
    else: 
        raise Exception("Fehler in oekonomie_vorbereiten(). Falsche Angabe Geschäftsmodell in if-Verzweigung")

    return eco