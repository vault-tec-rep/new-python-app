# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:57:20 2020

@author: Jonas Fuhrmann
"""


def jahresstromverbrauch_ermitteln(anzahl_bewohner, warmwasser):
    if warmwasser == 'Ja':
        if anzahl_bewohner == 1:
            jahresstromverbrauch = 2650
        elif anzahl_bewohner == 2:
            jahresstromverbrauch = 3750
        elif anzahl_bewohner == 3:
            jahresstromverbrauch = 4450
        elif anzahl_bewohner == 4:
            jahresstromverbrauch = 5250
        elif anzahl_bewohner == 5:
            jahresstromverbrauch = 6500
        elif anzahl_bewohner == 6:
            jahresstromverbrauch = 7700
        else:
            print("Funktion: Jahresstromverbrauch ermitteln. Problem: anzahl_bewohner nicht 1,2,3,4,5 oder 6.\
                  Setze Jahresstromverbrauch auf 2000")
            jahresstromverbrauch = 2000
    else:
        if anzahl_bewohner == 1:
            jahresstromverbrauch = 2250
        elif anzahl_bewohner == 2:
            jahresstromverbrauch = 2950
        elif anzahl_bewohner == 3:
            jahresstromverbrauch = 3150
        elif anzahl_bewohner == 4:
            jahresstromverbrauch = 5250
        elif anzahl_bewohner == 5:
            jahresstromverbrauch = 6500
        elif anzahl_bewohner == 6:
            jahresstromverbrauch = 7700
        else:
            print("Funktion: Jahresstromverbrauch ermitteln. Problem: anzahl_bewohner nicht 1,2,3,4,5 oder 6.\
                  Setze Jahresstromverbrauch auf 2000")
            jahresstromverbrauch = 2000
    return jahresstromverbrauch