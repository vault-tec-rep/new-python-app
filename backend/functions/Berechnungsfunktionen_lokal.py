#Berechnungsfunktionen der Geschäftsmodelle. Die Funktionen greifen auf weiter unten definierte Funktionen zurück. 
#%%
def berechnung(strompreis, kW, strompreissteigerung, kalkZins, jahresstromverbrauch, lastprofilNummer,
                einspeiseverguetungVektor, i_teilnehmer, spez_kosten_pv, geschäftsmodell, schule):
    import numpy as np
    import pandas as pd

    air_temp = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Air_Temp.npy', allow_pickle=True)
    GlobalStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\GlobalStr.npy', allow_pickle=True)
    DiffusStr = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\DiffusStr.npy', allow_pickle=True)
    zeit_vektor = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:59:00', freq='1min')
    [dirh, dhi, tamb, breite, laenge] = wetter_waehlen(air_temp, GlobalStr, DiffusStr)
    leistung_pv = berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, kW)
    
    if geschäftsmodell == 1: # Mieterstrom
        Lastprofile_Mfh = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_MFH.npy', allow_pickle=True)
        leistung_last = Lastprofile_Mfh[:, i_teilnehmer - 1]

        eco_eigenverbrauch = {}
        eco_mieterstrom = oekonomie_vorbereiten(strompreis, kW, strompreissteigerung, i_teilnehmer,spez_kosten_pv, geschäftsmodell)
        [barwert_mieterstrom, barwert_eigenverbrauch, eigenverbrauchsanteil, autarkiegrad] = oekonomie_berechnen(leistung_pv, leistung_last, eco_mieterstrom, eco_eigenverbrauch, kW, kalkZins, einspeiseverguetungVektor, geschäftsmodell, schule, jahresstromverbrauch)
        [durchschnittstag_pv, durchschnittstag_last] = durchschnittstag_berechnen(leistung_pv, leistung_last)
        return barwert_mieterstrom, barwert_eigenverbrauch, eigenverbrauchsanteil, autarkiegrad, durchschnittstag_pv, durchschnittstag_last

    elif geschäftsmodell == 2: # Gewerbe oder NWG
        Lastprofile_GW = np.load('D:\\Solarspeichersysteme\\09_Projekte\\2016_PV2City\\2018_10 Leitfaden Eigenverbrauch\\App-Entwicklung\\Unabhaengigkeitsrechner_Python\\Daten Wetter und Last\\Lastprofile_Gewerbe.npy', allow_pickle=True)
        leistung_last = Lastprofile_GW[:,lastprofilNummer]

        eco_mieterstrom= oekonomie_vorbereiten(strompreis, kW, strompreissteigerung, i_teilnehmer,spez_kosten_pv, 1)
        eco_eigenverbrauch = oekonomie_vorbereiten(strompreis, kW, strompreissteigerung, i_teilnehmer,spez_kosten_pv, 2)
        [barwert_mieterstrom, barwert_eigenverbrauch, eigenverbrauchsanteil, autarkiegrad] = oekonomie_berechnen(leistung_pv, leistung_last, eco_mieterstrom, eco_eigenverbrauch, kW, kalkZins, einspeiseverguetungVektor, geschäftsmodell, schule, jahresstromverbrauch)
        [durchschnittstag_pv, durchschnittstag_last] = durchschnittstag_berechnen(leistung_pv, leistung_last)
        return barwert_mieterstrom, barwert_eigenverbrauch, eigenverbrauchsanteil, autarkiegrad, durchschnittstag_pv, durchschnittstag_last

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

    #Annahmen für nachfolgende Berechnung
    azimuth = 90 #Osten (azimuth_2 wird Westen)
    aufstellwinkel = 15 
    logisch_doppelte_rechnung = 1 # Gibt es eine Ost_West_Aufständerung? --> Dann doppelte Berechnung mit Addition

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

def ephemeris(time, latitude, longitude, pressure=101325, temperature=12):
    import pandas as pd
    import numpy as np
    Latitude = latitude
    Longitude = -1 * longitude

    Abber = 20 / 3600.
    LatR = np.radians(Latitude)

    # the SPA algorithm needs time to be expressed in terms of
    # decimal UTC hours of the day of the year.

    # if localized, convert to UTC. otherwise, assume UTC.
    try:
        time_utc = time.tz_convert('UTC')
    except TypeError:
        time_utc = time

    # strip out the day of the year and calculate the decimal hour
    DayOfYear = time_utc.dayofyear
    DecHours = (time_utc.hour + time_utc.minute/60. + time_utc.second/3600. +
                time_utc.microsecond/3600.e6)

    # np.array needed for pandas > 0.20
    UnivDate = np.array(DayOfYear)
    UnivHr = np.array(DecHours)

    Yr = np.array(time_utc.year) - 1900
    YrBegin = 365 * Yr + np.floor((Yr - 1) / 4.) - 0.5

    Ezero = YrBegin + UnivDate
    T = Ezero / 36525.

    # Calculate Greenwich Mean Sidereal Time (GMST)
    GMST0 = 6 / 24. + 38 / 1440. + (
        45.836 + 8640184.542 * T + 0.0929 * T ** 2) / 86400.
    GMST0 = 360 * (GMST0 - np.floor(GMST0))
    GMSTi = np.mod(GMST0 + 360 * (1.0027379093 * UnivHr / 24.), 360)

    # Local apparent sidereal time
    LocAST = np.mod((360 + GMSTi - Longitude), 360)

    EpochDate = Ezero + UnivHr / 24.
    T1 = EpochDate / 36525.

    ObliquityR = np.radians(
        23.452294 - 0.0130125 * T1 - 1.64e-06 * T1 ** 2 + 5.03e-07 * T1 ** 3)
    MlPerigee = 281.22083 + 4.70684e-05 * EpochDate + 0.000453 * T1 ** 2 + (
        3e-06 * T1 ** 3)
    MeanAnom = np.mod((358.47583 + 0.985600267 * EpochDate - 0.00015 *
                       T1 ** 2 - 3e-06 * T1 ** 3), 360)
    Eccen = 0.01675104 - 4.18e-05 * T1 - 1.26e-07 * T1 ** 2
    EccenAnom = MeanAnom
    E = 0

    while np.max(abs(EccenAnom - E)) > 0.0001:
        E = EccenAnom
        EccenAnom = MeanAnom + np.degrees(Eccen)*np.sin(np.radians(E))

    TrueAnom = (
        2 * np.mod(np.degrees(np.arctan2(((1 + Eccen) / (1 - Eccen)) ** 0.5 *
                   np.tan(np.radians(EccenAnom) / 2.), 1)), 360))
    EcLon = np.mod(MlPerigee + TrueAnom, 360) - Abber
    EcLonR = np.radians(EcLon)
    DecR = np.arcsin(np.sin(ObliquityR)*np.sin(EcLonR))

    RtAscen = np.degrees(np.arctan2(np.cos(ObliquityR)*np.sin(EcLonR),
                                    np.cos(EcLonR)))

    HrAngle = LocAST - RtAscen
    HrAngleR = np.radians(HrAngle)

    SunAz = np.degrees(np.arctan2(-np.sin(HrAngleR),
                                  np.cos(LatR)*np.tan(DecR) -
                                  np.sin(LatR)*np.cos(HrAngleR)))
    SunAz[SunAz < 0] += 360

    SunEl = np.degrees(np.arcsin(
        np.cos(LatR) * np.cos(DecR) * np.cos(HrAngleR) +
        np.sin(LatR) * np.sin(DecR)))

    # make output DataFrame
    DFOut = pd.DataFrame(index=time_utc)
    DFOut['azimuth'] = SunAz
    DFOut['elevation'] = SunEl
    DFOut['zenith'] = 90 - SunEl
    DFOut.index = time

    return DFOut

def durchschnittstag_berechnen(pv_werte, last_werte):
    import numpy as np
    
    if len(last_werte < 525600):
        pv_werte2 = np.reshape(pv_werte, (96, 365))
        last_werte2 = np.reshape(last_werte, (96, 365))
    else:
        pv_werte2 = np.reshape(pv_werte, (1440, 365))
        last_werte2 = np.reshape(last_werte, (1440, 365))

    #Berechnung des Durchnittstages
    durchschnitsstag_pv = pv_werte2.sum(axis=1) / 365
    durchschnittstag_last = last_werte2.sum(axis=1) / 365

    return durchschnitsstag_pv, durchschnittstag_last

    




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

def oekonomie_berechnen(leistung_pv, leistung_last, eco_mieterstrom, eco_eigenverbrauch, kW, kalkulatorischer_zins, einspeiseverguetung_vektor, geschäftsmodell, schule, jahresstromverbrauch):
    # Imports
    import numpy as np
    import numpy_financial as npf
    from copy import deepcopy
    
    if geschäftsmodell == 1:
        #Annahmen
        mieterstrom_zuschlag = 'Ja' #Mieterstromzuschlag auf Ja. 
        betreiber = 'betreiber-0' #Eigentümer und Betreiber der Anlage ohne Pacht
        # Variablen statt festen Werten
        dt_min = 60  # Zeitschrittweite in Minuten

        # Berechnung
        kalkulatorischer_zins /= 100  # Prozent in dezimal

        e_pv2l = np.minimum(leistung_pv, leistung_last)  # in Watt!
        e_pv2g = leistung_pv - e_pv2l  # in Watt!
        # Grid to load
        e_g2l = leistung_last - leistung_pv  # in Watt!
        e_g2l[e_g2l <= 0] = 0  # in Watt!

        # Energiesummen
        summe_e_g2l = np.sum(e_g2l) / (dt_min*1000)  # Wattminuten in kWh umgerechnet
        summe_e_pv2l = np.sum(e_pv2l) / (dt_min*1000)  # in kWh
        summe_e_pv2g = np.sum(e_pv2g) / (dt_min*1000)  # in kWh
        summe_pvs = np.sum(leistung_pv) / (dt_min*1000)  # in kWh
        summe_last = np.sum(leistung_last) / (dt_min*1000)  # in kWh

        # Eigenverbrauchsanteil
        Eigenverbrauchsanteil = np.round((summe_e_pv2l / summe_pvs) * 100,1)
        # Autarkiegrad
        Autarkiegrad = np.round((summe_e_pv2l / summe_last)*100,1)

        # Erloese aus den Energieflüssen
        einspeiseverguetung = (np.minimum(10, kW) / kW * (einspeiseverguetung_vektor[0]/100) \
            + np.minimum(30, kW - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[1]/100) \
            + np.minimum(60, kW - np.minimum(30, kW - np.minimum(10, kW)) - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[2]/100))
        einspeiseverguetung -= 0.004  # Marktprämie abziehen
        ersparnis_pv2g = summe_e_pv2g * einspeiseverguetung
        
        # Mieterstromzuschlag
        if mieterstrom_zuschlag == 'Ja':
            if kW < 40:  # Zuschlag berechnen nach: für erste 40kW -8,5 ct, für danach nur -8,0 ct bis 750 kW
                c_mieterstromzuschlag = summe_e_pv2l * \
                    np.maximum((einspeiseverguetung - 0.085),0)
            else:
                c_mieterstromzuschlag = summe_e_pv2l * \
                    np.maximum((einspeiseverguetung - 0.08),0)
        else:
            c_mieterstromzuschlag = 0  

        C_Verwaltung = 100 / 1.19 # Euro pro Jahr und Teilnehmer
        # Rolle und die damit verbundenen Kosten
        if betreiber == 'betreiber-0':
            c_pacht = 0
        else:
            c_pacht = kW * 150/20

        #Gewinnrechnung
        #Nötige Vektoren
        umlage_vektor = eco_mieterstrom["umlage"]
        i_teilnehmer = eco_mieterstrom["i_teilnehmer"]
        strompreis_vektor = eco_mieterstrom["strompreis_vektor"]
        c_invest = eco_mieterstrom["invest"]
        kalkZins_vektor = np.zeros(20)
        kalkZins_vektor[0] = 1
        for i in range(19):
            kalkZins_vektor[i+1] = kalkZins_vektor[i] + kalkZins_vektor[i] * kalkulatorischer_zins
        
        betrieb_vektor = np.full((20,), eco_mieterstrom["betrieb"]) * kalkZins_vektor
        grundpreis_vektor = np.full((20,), eco_mieterstrom["grundpreis"]) * kalkZins_vektor

        # Berechnung über 20 Jahre:    
        # Annahme, damit der Mieterstrom vermarktet werden kann.
        c_Mieterstrompreis = 0.9 * strompreis_vektor

        # Zusammenrechnen der Kosten
        kosten_mieterstrom = -1 * summe_e_g2l*c_Mieterstrompreis / 1.19 \
            - betrieb_vektor /1.19 - umlage_vektor*summe_e_pv2l - \
            C_Verwaltung*i_teilnehmer - c_pacht
        gewinne_mieterstrom = summe_last*c_Mieterstrompreis /1.19 \
            + c_mieterstromzuschlag + ersparnis_pv2g \
            + grundpreis_vektor * i_teilnehmer / 1.19
            # Volleinspeisung vs. MS:
        gewinn_pv_20 = gewinne_mieterstrom + kosten_mieterstrom

        gewinn_nettobarwert = np.concatenate([[np.round(-1*c_invest, 0)], gewinn_pv_20])
        nettobarwert_mieterstrom = np.round(npf.npv(kalkulatorischer_zins, gewinn_nettobarwert), 0)

        nettobarwert_eigenverbrauch = 0
        return nettobarwert_mieterstrom, nettobarwert_eigenverbrauch, Eigenverbrauchsanteil, Autarkiegrad

    #---------------------------------------------------------------------------------------------------------------------------------------------
    elif geschäftsmodell == 2:
        #Vorbereitung
        betreiber = 'betreiber-0'
        #Verkleinern des PV-Vektors auf 15 Minuten
        leistung_pv_2 = leistung_pv[0::15].copy()
        #Umrechnung des kalkulatorischen Zinses
        kalkulatorischer_zins /= 100
        #Berechnung der Energiesummen, je nachdem ob Eigenverbrauchsanteil vorgegeben oder nicht
        if schule == 0:
            #Skalieren des Lastprofils
            leistung_last = np.divide(leistung_last, np.sum(leistung_last))
            leistung_last = leistung_last * jahresstromverbrauch*1000
            #Errechnen der Energieflüsse
            e_pv2l = np.minimum(leistung_pv_2, leistung_last)
            e_pv2g = leistung_pv_2 - e_pv2l
            e_g2l = leistung_last - leistung_pv_2 # Nur für Direktstrom relevantt
            e_g2l[e_g2l <= 0] = 0
            #Energiesummen
            summe_e_g2l = np.sum(e_g2l) / (4*1000)
            summe_e_pv2l = np.sum(e_pv2l) / (4*1000)
            summe_e_pv2g = np.sum(e_pv2g) / (4*1000)
            summe_pv = np.sum(leistung_pv_2) / (4*1000)
            summe_last = np.sum(leistung_last) / (4*1000)
            Eigenverbrauchsanteil = np.round((summe_e_pv2l / summe_pv) * 100)
            Autarkiegrad = np.round((summe_e_pv2l / summe_last)*100)
        elif schule == 1:
            #eigenverbrauchsanteil anhand Leitfaden berechnen
            Eigenverbrauchsanteil = 0.3 * ((kW/jahresstromverbrauch)^(-0.55))

            summe_pv = np.sum(leistung_pv) / (1000 * 60)
            summe_e_pv2l = summe_pv * Eigenverbrauchsanteil / 100
            summe_e_pv2g = summe_pv - summe_e_pv2l
            summe_e_g2l = np.sum(jahresstromverbrauch - summe_e_pv2l)
            Autarkiegrad = summe_e_pv2l / jahresstromverbrauch

        #Eigentliche Berechnung
        einspeiseverguetung = (np.minimum(10, kW) / kW * (einspeiseverguetung_vektor[0]/100) \
            + np.minimum(30, kW - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[1]/100) \
            + np.minimum(60, kW - np.minimum(30, kW - np.minimum(10, kW)) - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[2]/100))
        
        einspeiseverguetung -= 0.004  # Marktprämie abziehen
        ersparnis_pv2g = summe_e_pv2g * einspeiseverguetung

        #Schleife für Berechnung beider Geschäftsmodelle
        for geschäftsmodell_zähler in range(2):
            if geschäftsmodell_zähler == 0: #Hier wird Mieterstrom berechnet
                c_mieterstromzuschlag = 0 
                C_Verwaltung = 100 / 1.19 # Euro pro Jahr und Teilnehmer
                # Rolle und die damit verbundenen Kosten
                if betreiber == 'betreiber-0':
                    c_pacht = 0
                else:
                    c_pacht = kW * 150/20
                #Gewinnrechnung
                #Nötige Vektoren
                umlage_vektor = eco_mieterstrom["umlage"]
                i_teilnehmer = eco_mieterstrom["i_teilnehmer"]
                strompreis_vektor = eco_mieterstrom["strompreis_vektor"]
                c_invest = eco_mieterstrom["invest"]
                kalkZins_vektor = np.zeros(20)
                kalkZins_vektor[0] = 1
                for i in range(19):
                    kalkZins_vektor[i+1] = kalkZins_vektor[i] + kalkZins_vektor[i] * kalkulatorischer_zins
                    
                betrieb_vektor = np.full((20,), eco_mieterstrom["betrieb"]) * kalkZins_vektor
                grundpreis_vektor = np.full((20,), eco_mieterstrom["grundpreis"]) * kalkZins_vektor

                # Berechnung über 20 Jahre:    
                # Annahme, damit der Mieterstrom vermarktet werden kann.
                c_Mieterstrompreis = 0.9 * strompreis_vektor

                # Zusammenrechnen der Kosten
                kosten_mieterstrom = -1 * summe_e_g2l*c_Mieterstrompreis / 1.19 \
                    - betrieb_vektor /1.19 - umlage_vektor*summe_e_pv2l - \
                    C_Verwaltung*i_teilnehmer - c_pacht
                gewinne_mieterstrom = summe_last*c_Mieterstrompreis /1.19 \
                    + c_mieterstromzuschlag + ersparnis_pv2g \
                    + grundpreis_vektor * i_teilnehmer / 1.19
                    # Volleinspeisung vs. MS:
                gewinn_pv_20 =  gewinne_mieterstrom + kosten_mieterstrom   

                gewinn_nettobarwert = np.concatenate([[np.round(-1*c_invest, 0)], gewinn_pv_20])
                #ERGEBNIS DIREKTSTROM RECHNUNG!
                nettobarwert_mieterstrom = np.round(npf.npv(kalkulatorischer_zins, gewinn_nettobarwert), 0)
            
            elif geschäftsmodell_zähler == 1: #Hier wird Eigenvberbrauch berechnet
                #Nötige Vektoren
                umlage_vektor = eco_eigenverbrauch["umlage"]
                strompreis_vektor = eco_eigenverbrauch["strompreis_vektor"]
                c_invest = eco_eigenverbrauch["invest"]

                kalkZins_vektor = np.zeros(20)
                kalkZins_vektor[0] = 1
                for i in range(19):
                    kalkZins_vektor[i+1] = kalkZins_vektor[i] + kalkZins_vektor[i] * kalkulatorischer_zins
                betrieb_vektor = np.full((20,), eco_eigenverbrauch["betrieb"]) * kalkZins_vektor
                # Berechnung über 20 Jahre:   
                ersparnis_pv2l = summe_e_pv2l * strompreis_vektor

                if kW > 10:
                    gewinn_pv_20 = ersparnis_pv2l + ersparnis_pv2g - betrieb_vektor - umlage_vektor * 0.4*summe_e_pv2l
                else: 
                    gewinn_pv_20 = ersparnis_pv2l + ersparnis_pv2g - betrieb_vektor

                gewinn_nettobarwert = np.concatenate([[np.round(-1*c_invest, 0)], gewinn_pv_20])
                nettobarwert_eigenverbrauch = np.round(npf.npv(kalkulatorischer_zins, gewinn_nettobarwert), 0)

            else:
                raise Exception("Fehler in Geschäftsmodell Gewerbe: Interner Berechnungszähler falsch.")

        return nettobarwert_mieterstrom, nettobarwert_eigenverbrauch, Eigenverbrauchsanteil, Autarkiegrad 
    else:
        raise Exception("Fehler in oekonomie_berechnen. Geschäftsmodell falsch ausgewählt")

strompreis = 28
kW = 15
strompreissteigerung = 2
kalkZins = 2
jahresstromverbrauch = 30000
lastprofilNummer = 1
einspeiseverguetungVektor = [9.30, 9.05, 7.19]
i_teilnehmer = 5
mieterstromzuschlag = 'Ja'
spez_kosten_pv = 1450
schule = 0

geschäftsmodell = 2
[barwert_mieterstrom, barwert_eigenverbrauch, eigenverbrauchsanteil, autarkiegrad, durchschnittstag_pv, durchschnittstag_last] = berechnung(strompreis, kW, strompreissteigerung, 
                kalkZins, jahresstromverbrauch, lastprofilNummer,
                einspeiseverguetungVektor, i_teilnehmer, spez_kosten_pv, geschäftsmodell, schule)
# %%
