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


def bssim(p_pv, e_bat, pd):
    import numpy as np
    from numba import jit

    # Achtung, p_ac2bat_in und p_bat2ac_out sind in Abhängigkeit von e_bat!

    # Zeitschrittsimulation Defintion

    @jit(nopython=True)
    def schleife(tend, p_pv, e_bat):
        # Definition der Parameter
        eta_ac2bat = np.float32(0.93)
        eta_bat2ac = np.float32(0.93)
        dt = np.float32(1/60)  # in hours
        p_ac2bat_in = e_bat  # aus kWh mache kW
        p_bat2ac_out = e_bat  # aus kWh mache kW
        eta_bat = np.float32(0.93)
        # Vorinitialisieren
        soc = np.zeros(tend, dtype=np.float32)
        ebat = np.zeros(tend, dtype=np.float32)
        pbatin = np.zeros(tend, dtype=np.float32)
        pbatout = np.zeros(tend, dtype=np.float32)
        pbat = np.zeros(tend, dtype=np.float32)
        pbs = np.zeros(tend, dtype=np.float32)
        if e_bat > 0:
            tstart = 1
            diff = tend - tstart

            for t in range(diff):
                if pd[t] > 0:
                    pbatin[t] = np.minimum(pd[t], p_ac2bat_in*1000)*eta_ac2bat
                    pbatin[t] = np.minimum(pbatin[t],
                                           e_bat*1000*(1-soc[t-1])/dt/eta_bat)

                elif pd[t] < 0:
                    pbatout[t] = np.maximum(pd[t],
                                            - p_bat2ac_out*1000)/eta_bat2ac
                    pbatout[t] = -1*np.minimum(-1*pbatout[t],
                                               e_bat*1000*soc[t-1]/dt)

                pbat[t] = pbatin[t] + pbatout[t]  # wozu?
                pbs[t] = pbatin[t] / eta_ac2bat + pbatout[t] * eta_bat2ac
                ebat[t] = ebat[t-1] + (pbatin[t]*eta_bat+pbatout[t])/1000*dt
                soc[t] = ebat[t] / e_bat
        return pbs
    tend = np.size(pd)
    pbs_out = schleife(tend, p_pv, e_bat)
    return pbs_out


def wetter_waehlen(standort, tamb, global_str, dhi):


    """
    Wählt aus aus dem Standort die Wetterstation aus

    Eingangsparameter: 
    standort: String der Wetterstation
    tamb: Matrix der Umgebungstemperaturen
    global_str: Matrix der Globalstrahlungen
    dhi: Diffus Horizontale Strahlung (Matrix)

    Ausgangsparameter
    dirh_extracted: Vektor der direkt-horizontalen Einstrahlung 
    dhi_extracted: Vektor der diffus-horizontalen Einstrahlung
    tamb_extracted: Vektor der Umgebungsstemperatur
    breite: Geographische Breite
    laenge: Geographische Laenge
    """

    dirh = global_str - dhi

    if standort == '1':
        breite = 53.079
        laenge = 8.802
        dhi_extracted = dhi[:, 3]
        dirh_extracted = dirh[:, 3]
        tamb_extracted = tamb[:, 3]
    elif standort == '2':
        breite = 52.388
        laenge = 13.065
        dhi_extracted = dhi[:, 14]
        dirh_extracted = dirh[:, 14]
        tamb_extracted = tamb[:, 14]
    elif standort == '3':
        breite = 52.304
        laenge = 10.514
        dhi_extracted = dhi[:, 2]
        dirh_extracted = dirh[:, 2]
        tamb_extracted = tamb[:, 2]
    elif standort == '4':
        breite = 48.776
        laenge = 9.183
        dhi_extracted = dhi[:, 19]
        dirh_extracted = dirh[:, 19]
        tamb_extracted = tamb[:, 19]
    elif standort == '6':
        breite = 48.396
        laenge = 11.774
        dhi_extracted = dhi[:, 21]
        dirh_extracted = dirh[:, 21]
        tamb_extracted = tamb[:, 21]
    else:
        print("wetter_waehlen: Fehler in der Standortauswahl.")

    return dirh_extracted, dhi_extracted, tamb_extracted, breite, laenge


def pv_werte_waehlen(dachart_2, dachkonfiguration_2, welches_dach_2):
    """
    Bestimmt aus der Dachkonfiguration eine logische Aussage

    Eingangsparameter
    dachart: Art des Dachs (Flach / Schraeg)
    dachkonfiguration: Hintereinander oder Trapez
    welches_dach: Eine Dachhaelfte oder beide Dachhaelften

    Ausgangsparameter
    logisch_doppelte_rechnun: 1 oder 0 je nachdem, ob die installierte
    Leistung sich auf 2 entgegengesetzte Richtungen auftzeilt (z.B: O/W)  
    """
    
    if dachart_2 == '1':
        dachart = 'Flachdach'
    else: 
        dachart = 'Schraegdach'

    if dachkonfiguration_2 == '1':
        dachkonfiguration = 'Trapez'
    else: 
        dachkonfiguration = 'Hintereinander'

    if welches_dach_2 == '1':
        welches_dach = 'Eine Dachhaelfte'
    else: 
        welches_dach = 'Beide Dachhaelften'

    if dachart == 'Schraegdach':
        if welches_dach == 'Eine Dachhaelfte':
            logisch_doppelte_rechnung = 0
        elif welches_dach == 'Beide Dachhaelften':
            logisch_doppelte_rechnung = 1
        else:
            print("pv_werte_waehlen: Fehler im Abzweig schraegdach bei der Auswahl.")
    elif dachart == 'Flachdach':
        if dachkonfiguration == 'Trapez':
            logisch_doppelte_rechnung = 1
        elif dachkonfiguration == 'Hintereinander':
            logisch_doppelte_rechnung = 0
        else:
            print("pv_werte_waehlen: Fehler im Abzweig flachdach bei der Auswahl.")

 
    return logisch_doppelte_rechnung

def berechnung_pv_vektor(dirh, dhi, tamb, zeit_vektor, breite, laenge, azimuth, aufstellwinkel, kW, logisch_doppelte_rechnung):
    import numpy as np
    import copy
    from Allgemeine_Funktionen import poa, pv_syst

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
