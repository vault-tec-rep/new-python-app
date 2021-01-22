def oekonomie_vorbereiten_ev_speicher(strompreis, kW, strompreissteigerung, speicher_kWh, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten):
    """
    Erstellt ein Eco-Struct mit oekonomischen Parametern (Eigenverbrauch Eigenheim)
    Verwendet für Einfamilienhaus mit Eigenverbrauch

    Eingangsparameter: 
    strompreis: Strompreis in ct/kWh
    kW: Installierte PV Leistung
    strompreissteigerung: Jährliche Strompreissteigerung in %
    speicher_kWh: Speicherkapazität in kWh

    Ausgabeparameter: 
    eco: Struct mit oekonomischen Parametern
    """
    # imports
    import numpy as np

    #Berechnung
    strompreis /= 100
    strompreissteigerung /= 100
    strompreis_vektor = np.zeros(20)
    eco = {}

    for zahl in range(20):
        if zahl > 0:
            strompreis *= (1 + strompreissteigerung)
        strompreis_vektor[zahl] = strompreis

    # Betriebskosten PV
    if absolute_kosten[0] == 1:
        eco["fix"] = betrieb_parameter[0]
        if kW > 8:
            eco["fix"] = betrieb_parameter[0] + 21
        eco["betrieb"] = eco["fix"] + kW * betrieb_parameter[1]
    else:
        eco["betrieb"] = absolute_kosten[2]

    # Kosten Speicher
    if speicher_kWh == 0:
        invest_speicher = 0
    else:
        invest_speicher = np.round(
            (2652.94 * speicher_kWh**(-0.3949))*speicher_kWh*1.19, 2)
    # Investkosten
    if absolute_kosten[0] == 1:

        if kW >= 30:
            invest_pv = np.round((invest_parameter[0]) * kW**invest_parameter[1] * kW * 1.19, 2) + 3000
        else: 
            invest_pv = np.round((invest_parameter[0]) * kW**invest_parameter[1] * kW * 1.19, 2)

        eco["invest"] = np.round(1.5*invest_speicher + invest_pv, 2) + zusatzkosten
    else: 
        eco["invest"] = absolute_kosten[1]
    # EEG Umlage 2020 - 2035 nach Agora Energiewende vom. 17.08.2020, danach konstant angenommen
    eco["umlage"] = np.array([0.06756, 0.06919, 0.06591, 0.06416, 0.06348, 0.06163, 0.05799, 0.05326, 0.04982, 0.04591,
                              0.04106, 0.03362, 0.02654, 0.0234, 0.02110, 0.02110, 0.02110, 0.02110, 0.02110, 0.02110])
    eco["strompreis_vektor"] = strompreis_vektor
    return eco

def last_waehlen(jahresstromverbrauch, lastprofil_matrix,
                 wirkleistung_jahr_sortiert, index_last):
    import numpy as np
    index_min = np.argmin(np.absolute(
        jahresstromverbrauch - wirkleistung_jahr_sortiert))
    stelle_lastprofil = index_last[0, index_min]
    lastprofil = lastprofil_matrix[:, stelle_lastprofil]
    return lastprofil
 

def oekonomie_berechnen_ev_speicher(leistung_pv, leistung_last, eco, kW, kalkulatorischer_zins, speicher_kWh, einspeiseverguetung_vektor):
    #Imports
    import numpy as np
    import numpy_financial as npf
    from Allgemeine_Funktionen import bssim
    
    #Berechnung
    kalkulatorischer_zins /= 100

    pd = leistung_pv - leistung_last
    pbs = bssim(kW, speicher_kWh, pd)
    # Netzleistung bestimmen
    pg = leistung_pv - leistung_last - pbs

    el = np.sum(leistung_last)/1000/60
    epvs = np.sum(leistung_pv)/1000/60
    epvs2l = np.sum(np.minimum(leistung_pv, leistung_last))/60/1000
    eac2bs = np.sum(np.maximum(0, pbs))/60/1000
    ebs2ac = np.sum(np.absolute(np.minimum(0, pbs)))/60/1000
    eac2g = np.sum(np.maximum(0, pg))/60/1000

    # Eigenverbrauchsanteil
    Eigenverbrauchsanteil = np.round(
        np.divide((epvs2l + eac2bs), epvs) * 100, 0)

    # Autarkiegrad
    Autarkiegrad = np.round(np.divide((epvs2l + ebs2ac), el) * 100, 0)

    # Erloese und Ersparnisse
    einspeiseverguetung =  np.minimum(10, kW) / kW * (einspeiseverguetung_vektor[0]/100) \
        + np.minimum(30, kW - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[1]/100)\
        + np.minimum(60, kW - np.minimum(30, kW - np.minimum(10, kW)
                                     ) - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[2]/100)
    ersparnis_pv2g = eac2g * einspeiseverguetung                                 
    eco["ersparnis_pv2g"] = ersparnis_pv2g

    # Gewinn für 20 Jahre
    gewinn_pv_20 = np.zeros(20)
    gewinnkurve = np.zeros(21)
    gewinnkurve[0] = np.round(-1*eco["invest"], 0)
    eco_umlage = eco["umlage"]

    stromgestehung_zaehler = np.zeros(20)
    stromgestehung_nenner = np.zeros(20)

    for n in range(20):
        if n > 0:
            eco["betrieb"] = eco["betrieb"] + eco["betrieb"]*kalkulatorischer_zins
        ersparnis_pv2l = (epvs2l + ebs2ac) * eco["strompreis_vektor"][n]

        if kW > 10:
            gewinn_pv_20[n] = ersparnis_pv2l + eco["ersparnis_pv2g"] - eco["betrieb"] - eco_umlage[n] *0.4*(epvs2l+ebs2ac)
        else:
            gewinn_pv_20[n] = ersparnis_pv2l + eco["ersparnis_pv2g"] - eco["betrieb"]

        gewinnkurve[n+1] = gewinnkurve[n] + gewinn_pv_20[n]

        #Stromgestehungskosten Zaehler und Nenner
        if n == 0:
            stromgestehung_zaehler[n] = (eco["invest"] + eco["betrieb"]) / ((1 + kalkulatorischer_zins)**n)
        stromgestehung_nenner[n] = epvs / ((1 + kalkulatorischer_zins)**n)
    
    gewinn_nettobarwert = np.concatenate([[gewinnkurve[0]], gewinn_pv_20])
    nettobarwert = np.round(npf.npv(kalkulatorischer_zins, gewinn_nettobarwert), 0)

    if kW == 0:
        rendite = 0
        nettobarwert = 0
    else:
        rendite = np.round(npf.irr(np.concatenate([[gewinnkurve[0]], gewinn_pv_20])), 2)
        rendite *= 100
    
    #Stromgestehungskosten
    zaehler = np.sum(stromgestehung_zaehler)
    nenner = np.sum(stromgestehung_nenner)
    stromgestehungskosten = np.round((zaehler / nenner) * 100, 1)

    return nettobarwert, rendite, gewinnkurve, Eigenverbrauchsanteil, Autarkiegrad, stromgestehungskosten