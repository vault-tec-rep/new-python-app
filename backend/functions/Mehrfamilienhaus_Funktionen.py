def oekonomie_vorbereiten_ms(strompreis, kW, strompreissteigerung, i_teilnehmer, invest_parameter, betrieb_parameter, zusatzkosten, absolute_kosten):
    # Imports
    import numpy as np

    # Berechnung
    strompreis /= 100  # Angabe als netto
    strompreissteigerung /= 100
    strompreis_vektor = np.zeros(20)
    eco = {}
    # das geht bestimmt auch über Vektoren, die elementweise multipliziert werden:
    for zahl in range(20):
        if zahl > 0:
            strompreis *= (1 + strompreissteigerung)
        strompreis_vektor[zahl] = strompreis


    # Betriebskosten Mieterstrom nach Kelm2019:
    # c_Betrieb_jaehrl = 17 * kW  # 17 real 
    c_grundpreis = 100  # Quelle Kelm19 sagt: 50-100
    # c_messstelle = 100
    eco["grundpreis"] = c_grundpreis
    eco["i_teilnehmer"] = i_teilnehmer

    if kW <= 7:
        c_zaehler = 60
    elif kW > 7 and kW <= 15:
        c_zaehler = 100
    elif kW > 15 and kW <= 30:
        c_zaehler = 130
    elif kW > 30:
        c_zaehler = 200

    eco["betrieb"] = betrieb_parameter[0] + c_zaehler + betrieb_parameter[1] * kW # + c_messstelle * i_teilnehmer
    # Berni neu:
    c_messsystem_einmal_Kelm19 = 125 * i_teilnehmer # einmalig: Einmalige Investitionsausgaben für die Umsetzung des Messkonzepts in Höhe von 100 bis 150 E uro pro Teilnehmer
    c_messsystem_jaehrlich_Kelm19 = 75 * i_teilnehmer # jährlich: Kosten für Messstellenbetrieb, Abrechnung, Rechnungstellung und Vertrieb in Höhe von 50 bis 100 Euro pro Teilnehmer und Jahr
    eco["messsystem_Kelm19"]= c_messsystem_einmal_Kelm19 + 20*c_messsystem_jaehrlich_Kelm19
    
    eco["betrieb_Kelm19"] = 17 * kW  # real konstant, jährlich

    if kW < 7:
        eco["betrieb_JB"] = betrieb_parameter[0] + betrieb_parameter[1] * kW
    else:
            eco["betrieb_JB"] = betrieb_parameter[0] + 21 + betrieb_parameter[1] * kW
    
    if absolute_kosten[0] == 1:
        eco["betrieb_JB"] = eco["betrieb_JB"] + c_zaehler  # stimmt das so?
    else: 
        eco["betrieb_JB"] = absolute_kosten[2]
    
    # Investkosten
    if absolute_kosten[0] == 1:
        invest_zaehler = 150*i_teilnehmer  # Quelle Kelm sagt: 100-150
        invest_pv = invest_parameter[0]*kW**(invest_parameter[1])*kW  # netto, also ohne: *1.19 oder?
    
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


def oekonomie_berechnen_ms(leistung_pv, leistung_last, eco, kW, mieterstrom_zuschlag, kalkulatorischer_zins, betreiber, einspeiseverguetung_vektor):
    # Imports
    import numpy as np
    import numpy_financial as npf
    
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
        + np.minimum(60, kW - np.minimum(30, kW - np.minimum(10, kW)
                                         ) - np.minimum(10, kW)) / kW * (einspeiseverguetung_vektor[2]/100))
    einspeiseverguetung -= 0.004  # Marktprämie abziehen
    ersparnis_pv2g = summe_e_pv2g * einspeiseverguetung
    
    # Gewinn 20 Jahre
    gewinn_pv_20 = np.zeros(20)
    gewinnkurve = np.zeros(21)
    gewinnkurve[0] = np.round(-1*eco["invest"], 0)
    

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

    stromgestehung_zaehler = np.zeros(20)
    stromgestehung_nenner = np.zeros(20)
    # Berechnung über 20 Jahre:    
    for n in range(20):

        if n > 0:  # Achtung, hier werden die aus eco_vorbereiten stammenden Werte überschrieben mit Inflation
            eco["betrieb"] += eco["betrieb"]*kalkulatorischer_zins
            eco["grundpreis"] += eco["grundpreis"] * kalkulatorischer_zins

        # Annahme, damit der Mieterstrom vermarktet werden kann.
        c_Mieterstrompreis = 0.9 * eco["strompreis_vektor"][n]

        # Bonusberechnung (nicht in Oekonomie_berechnen_MS_JB): lcoe
        #Stromgestehungskosten Zaehler und Nenner
        if n == 0:
            stromgestehung_zaehler[n] = (eco["invest"] + eco["betrieb"]) / ((1 + kalkulatorischer_zins)**n)
        else:
                #! die Betriebskosten muss ich doch auch jährlich abzinsen!
                stromgestehung_zaehler[n] = (eco["betrieb"]) / ((1 + kalkulatorischer_zins)**n)       
        stromgestehung_nenner[n] = summe_pvs / ((1 + kalkulatorischer_zins)**n)
        # Ende lcoe


        # Zusammenrechnen der Kosten
        kosten_mieterstrom = -1 * summe_e_g2l*1*c_Mieterstrompreis / 1.19 \
            - eco["betrieb"] /1.19 - eco["umlage"][n]*summe_e_pv2l - \
            C_Verwaltung*eco["i_teilnehmer"] - c_pacht
        gewinne_mieterstrom = summe_last*1*c_Mieterstrompreis /1.19 \
            + c_mieterstromzuschlag + ersparnis_pv2g \
            + eco["grundpreis"] * eco["i_teilnehmer"] / 1.19
        # Volleinspeisung vs. MS:
        gewinn_pv_20[n] = np.maximum(summe_pvs * einspeiseverguetung - eco["betrieb"] /1.19,\
            gewinne_mieterstrom + kosten_mieterstrom)  # Mieterstrom
        gewinnkurve[n+1] = gewinnkurve[n] + gewinn_pv_20[n]  # kumuliert
    # Schleifenende 20 Jahre

    gewinn_nettobarwert = np.concatenate([[gewinnkurve[0]], gewinn_pv_20])
    nettobarwert = np.round(npf.npv(kalkulatorischer_zins, gewinn_nettobarwert), 0)

    if kW == 0:  # warum fragen wir das ab?!
        rendite = 0
        nettobarwert = 0
    else:
        rendite = npf.irr(gewinn_nettobarwert)
        rendite = np.round(rendite*100, 2)
    
    #BS: soweit OK
    
    #Stromgestehungskosten
    zaehler = np.sum(stromgestehung_zaehler)
    nenner = np.sum(stromgestehung_nenner)
    stromgestehungskosten = np.round((zaehler / nenner) * 100, 1)

    return nettobarwert, rendite, gewinnkurve, Eigenverbrauchsanteil, Autarkiegrad, stromgestehungskosten
