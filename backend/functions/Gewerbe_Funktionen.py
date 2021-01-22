def oekonomie_vorbereiten_gw(strompreis, kW, strompreissteigerung, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten):
    # Imports
    import numpy as np

    # Berechnung
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

    # Invest
    if absolute_kosten[0] == 1:
        if kW >= 30:
            eco["invest"] = np.round(invest_parameter[0] * kW ** (invest_parameter[1]) * kW * 1.19, 2) + 3000 + zusatzkosten
        else: 
            eco["invest"] = np.round(invest_parameter[0] * kW ** (invest_parameter[1]) * kW * 1.19, 2) + zusatzkosten
    else: 
        eco["invest"] = absolute_kosten[1]
    # EEG Umlage 2020 - 2035 nach Agora Energiewende vom. 17.08.2020, danach konstant angenommen
    eco["umlage"] = np.array([0.06756, 0.06919, 0.06591, 0.06416, 0.06348, 0.06163, 0.05799, 0.05326, 0.04982, 0.04591,
                              0.04106, 0.03362, 0.02654, 0.0234, 0.02110, 0.02110, 0.02110, 0.02110, 0.02110, 0.02110])
    eco["strompreis_vektor"] = strompreis_vektor
    return eco


def oekonomie_vorbereiten_gw_ds(strompreis, kW, strompreissteigerung, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten):
    # Imports
    import numpy as np

    # Berechnung
    strompreis /= 100
    strompreissteigerung /= 100
    strompreis_vektor = np.zeros(20)
    eco = {}

    for zahl in range(20):
        if zahl > 0:
            strompreis *= (1 + strompreissteigerung)
        strompreis_vektor[zahl] = strompreis

    # Betriebskosten PV
    c_grundpreis = 100
    c_messstelle = 100
    eco["grundpreis"] = c_grundpreis
    eco["i_teilnehmer"] = 1
    i_teilnehmer = 1

    if kW <= 7:
        c_zaehler = 60
    elif kW > 7 and kW <= 15:
        c_zaehler = 100
    elif kW > 15 and kW <= 30:
        c_zaehler = 130
    elif kW > 30:
        c_zaehler = 200

    if absolute_kosten[0] == 1:
        eco["betrieb"] = betrieb_parameter[0] + c_zaehler + betrieb_parameter[1] * kW + c_messstelle
    else:
        eco["betrieb"] = absolute_kosten[2]

    #Investkosten
    if absolute_kosten[0] == 1:

        invest_zaehler = 300*i_teilnehmer
        invest_pv = invest_parameter[0]*kW**(invest_parameter[1])*kW*1.19
        if kW >= 30:
            eco["invest"] = np.round(invest_pv + invest_zaehler, 2) + 3000 + zusatzkosten
        else: 
            eco["invest"] = np.round(invest_pv + invest_zaehler, 2) + zusatzkosten
    else: 
        eco["invest"] = absolute_kosten[1]

    # EEG Umlage 2020 - 2035 nach Agora Energiewende vom. 17.08.2020, danach konstant angenommen
    eco["umlage"] = np.array([0.06756, 0.06919, 0.06591, 0.06416, 0.06348, 0.06163, 0.05799, 0.05326, 0.04982, 0.04591,
                              0.04106, 0.03362, 0.02654, 0.0234, 0.02110, 0.02110, 0.02110, 0.02110, 0.02110, 0.02110])
    eco["strompreis_vektor"] = strompreis_vektor
    return eco


def oekonomie_vorbereiten_gw_ve(kW, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten):
    import numpy as np

    eco = {}
    # Betriebskosten PV
    if absolute_kosten[0] == 1:
        eco["fix"] = betrieb_parameter[0]
        if kW > 8:
            eco["fix"] = betrieb_parameter[0] + 21
        eco["betrieb"] = eco["fix"] + kW * betrieb_parameter[1]
    else: 
        eco["betrieb"] = absolute_kosten[2]

    # Invest
    if absolute_kosten[0] == 1:
        if kW >= 30: 
            eco["invest"] = np.round(invest_parameter[0] * kW ** (invest_parameter[1]) * kW * 1.19, 2) + 3000 + zusatzkosten
        else: 
            eco["invest"] = np.round(invest_parameter[0] * kW ** (invest_parameter[1]) * kW * 1.19, 2) + zusatzkosten
    else:
        eco["invest"] = absolute_kosten[1]

        
    return eco


def oekonomie_berechnen_gw_ev(leistung_pv, leistung_last, eco, kW, kalkulatorischer_zins,
                                Jahresstromverbrauch, einspeiseverguetung_vektor, eigenverbrauchsanteil, lastprofil_verwenden):
    # Imports
    import numpy as np
    import numpy_financial as npf
    import copy
    
    # Anpassen des PV-Vektors
    leistung_pv_2 = leistung_pv[0::15].copy()
    if lastprofil_verwenden == True:
        # Skalieren des Lastprofils
        leistung_last = np.divide(leistung_last, np.sum(leistung_last))
        leistung_last = leistung_last * Jahresstromverbrauch*1000

        e_pv2l = np.minimum(leistung_pv_2, leistung_last)
        e_pv2g = leistung_pv_2 - e_pv2l
        # Energiesummen
        summe_e_pv2l = np.sum(e_pv2l) / (1000 * 4)
        summe_e_pv2g = np.sum(e_pv2g) / (1000 * 4)
        summe_last = np.sum(leistung_last) / (1000 * 4)
        summe_pv = np.sum(leistung_pv_2) / (1000 * 4)
        # Eigenverbrauchsanteil
        Eigenverbrauchsanteil = np.round((summe_e_pv2l / summe_pv) * 100)
        # Autarkiegrad
        Autarkiegrad = np.round((summe_e_pv2l / summe_last) * 100)
    else:
        summe_pv = np.sum(leistung_pv) / (1000 * 60)
        summe_e_pv2l = summe_pv * eigenverbrauchsanteil / 100
        summe_e_pv2g = summe_pv - summe_e_pv2l
        Autarkiegrad = summe_e_pv2l / Jahresstromverbrauch
        Eigenverbrauchsanteil = eigenverbrauchsanteil

    # Berechnung
    kalkulatorischer_zins /= 100
    
    einspeiseverguetung = (np.minimum(10, kW) / kW * (einspeiseverguetung_vektor[0]/100) \
        + np.minimum(30, kW - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[1]/100) \
        + np.minimum(60, kW - np.minimum(30, kW - np.minimum(10, kW)
                                         ) - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[2]/100))
    ersparnis_pv2g = summe_e_pv2g * einspeiseverguetung                                     
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
            eco["betrieb"] += eco["betrieb"]*kalkulatorischer_zins
        ersparnis_pv2l = summe_e_pv2l * eco["strompreis_vektor"][n]

        if kW > 10:
            gewinn_pv_20[n] = ersparnis_pv2l + eco["ersparnis_pv2g"] - \
                eco["betrieb"] - eco_umlage[n] * 0.4*summe_e_pv2l
        else:
            gewinn_pv_20[n] = ersparnis_pv2l + \
                eco["ersparnis_pv2g"] - eco["betrieb"]

        gewinnkurve[n+1] = gewinnkurve[n] + gewinn_pv_20[n]

        #Stromgestehungskosten Zaehler und Nenner
        if n == 0:
            stromgestehung_zaehler[n] = (eco["invest"] + eco["betrieb"]) / ((1 + kalkulatorischer_zins)**n)
        stromgestehung_nenner[n] = summe_pv / ((1 + kalkulatorischer_zins)**n)

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


def oekonomie_berechnen_gw_ds(leistung_pv, leistung_last, eco, kW, kalkulatorischer_zins, betreiber,
                                Jahresstromverbrauch, einspeiseverguetung_vektor, eigenverbrauchsanteil, lastprofil_verwenden):
    # Imports
    import numpy as np
    import numpy_financial as npf
    import copy

    leistung_pv_2 = leistung_pv[0::15].copy()
    if lastprofil_verwenden == True:
        # Skalieren des Lastprofils
        leistung_last = np.divide(leistung_last, np.sum(leistung_last))
        leistung_last = leistung_last * Jahresstromverbrauch*1000
        # Anpassen des PV-Vektors
        e_pv2l = np.minimum(leistung_pv_2, leistung_last)
        e_pv2g = leistung_pv_2 - e_pv2l
        # Grid to load
        e_g2l = leistung_last - leistung_pv_2
        e_g2l[e_g2l <= 0] = 0

        # Energiesummen
        summe_e_g2l = np.sum(e_g2l) / (4*1000)
        summe_e_pv2l = np.sum(e_pv2l) / (4*1000)
        summe_e_pv2g = np.sum(e_pv2g) / (4*1000)
        summe_pv = np.sum(leistung_pv_2) / (4*1000)
        summe_last = np.sum(leistung_last) / (4*1000)
        Eigenverbrauchsanteil = np.round((summe_e_pv2l / summe_pv) * 100)
        Autarkiegrad = np.round((summe_e_pv2l / summe_last)*100)
    else: 
        summe_pv = np.sum(leistung_pv) / (1000 * 60)
        summe_e_pv2l = summe_pv * eigenverbrauchsanteil / 100
        summe_e_pv2g = summe_pv - summe_e_pv2l
        Autarkiegrad = summe_e_pv2l / Jahresstromverbrauch
        Eigenverbrauchsanteil = eigenverbrauchsanteil
        summe_e_g2l = np.sum(Jahresstromverbrauch - summe_e_pv2l)
    # Berechnung
    kalkulatorischer_zins /= 100

    # Erloese aus den Energieflüssen
    einspeiseverguetung = (np.minimum(10, kW) / kW * (einspeiseverguetung_vektor[0]/100) \
        + np.minimum(30, kW - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[1]/100) \
        + np.minimum(60, kW - np.minimum(30, kW - np.minimum(10, kW)
                                         ) - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[2]/100))
    ersparnis_pv2g = summe_e_pv2g * einspeiseverguetung

    # Gewinn 20 Jahre
    gewinn_pv_20 = np.zeros(20)
    gewinnkurve = np.zeros(21)
    gewinnkurve[0] = np.round(-1*eco["invest"], 0)
    eco_umlage = eco["umlage"]

    stromgestehung_zaehler = np.zeros(20)
    stromgestehung_nenner = np.zeros(20)

    for n in range(20):
        c_mieterstromzuschlag = 0

        if n > 0:
            eco["betrieb"] += eco["betrieb"]*kalkulatorischer_zins
            eco["grundpreis"] += eco["grundpreis"] * kalkulatorischer_zins
        # Rolle und die damit verbundenen kosten
        if betreiber == 'betreiber-0':
            c_pacht = 0
        else:
            c_pacht = kW * 150/20

        # Zusammenrechnen der Kosten
        kosten_mieterstrom = - summe_e_g2l*0.91*eco["strompreis_vektor"][n] \
            - eco["betrieb"] - eco_umlage[n]*summe_e_pv2l - \
            300*eco["i_teilnehmer"] - c_pacht
        gewinne_mieterstrom = summe_last * 0.95 * eco["strompreis_vektor"][n] / 1.19 + c_mieterstromzuschlag + ersparnis_pv2g \
            + eco["grundpreis"] * eco["i_teilnehmer"] / 1.19

        gewinn_pv_20[n] = gewinne_mieterstrom + kosten_mieterstrom
        gewinnkurve[n+1] = gewinnkurve[n] + gewinn_pv_20[n]

        #Stromgestehungskosten Zaehler und Nenner
        if n == 0:
            stromgestehung_zaehler[n] = (eco["invest"] + eco["betrieb"]) / ((1 + kalkulatorischer_zins)**n)
        stromgestehung_nenner[n] = summe_pv / ((1 + kalkulatorischer_zins)**n)

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


def oekonomie_berechnen_gw_ve(leistung_pv, eco, kW, kalkulatorischer_zins, einspeiseverguetung_vektor):
    # Imports
    import numpy as np
    import numpy_financial as npf
    import copy
    # Berechnung
    kalkulatorischer_zins /= 100

    summe_e_pv2g = np.sum(leistung_pv) / (60 * 1000)

    # Erloese aus den Energieflüssen
    einspeiseverguetung = (np.minimum(10, kW) / kW * (einspeiseverguetung_vektor[0]/100) \
        + np.minimum(30, kW - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[1]/100) \
        + np.minimum(60, kW - np.minimum(30, kW - np.minimum(10, kW)
                                         ) - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[2]/100))
    ersparnis_pv2g = summe_e_pv2g * einspeiseverguetung

    # Gewinn 20 Jahre
    gewinn_pv_20 = np.zeros(20)
    gewinnkurve = np.zeros(21)
    gewinnkurve[0] = np.round(-1*eco["invest"], 0)

    stromgestehung_zaehler = np.zeros(20)
    stromgestehung_nenner = np.zeros(20)

    for n in range(20):
        if n > 0:
            eco["betrieb"] += eco["betrieb"]*kalkulatorischer_zins
        gewinn_pv_20[n] = ersparnis_pv2g - eco["betrieb"]
        gewinnkurve[n+1] = gewinnkurve[n] + gewinn_pv_20[n]

        #Stromgestehungskosten Zaehler und Nenner
        if n == 0:
            stromgestehung_zaehler[n] = (eco["invest"] + eco["betrieb"]) / ((1 + kalkulatorischer_zins)**n)
        stromgestehung_nenner[n] = summe_e_pv2g / ((1 + kalkulatorischer_zins)**n)

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

    return nettobarwert, rendite, gewinnkurve, stromgestehungskosten
