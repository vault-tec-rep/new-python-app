from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
#Für Deployment
#from Berechnung_Funktionen import berechnung_ev, berechnung_ms, berechnung_gw_ev, berechnung_gw_ds, berechnung_gw_ve
#Für ng-serve testen
from Berechnung_Funktionen_Lokal import berechnung_ev, berechnung_ms, berechnung_gw_ev, berechnung_gw_ds, berechnung_gw_ve
app = Flask(__name__)
CORS(app)


@app.route("/ev", methods = ["POST", "OPTIONS"])
def ev():
    if request.method == "OPTIONS": # CORS preflight
            return _build_cors_preflight_response()
    elif request.method == "POST": #Actual request following the preflight
        datei = request.get_json()
        [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = berechnung_ev(datei.get("wetterstation"), datei.get("kW"), datei.get("jahresstromverbrauch"), datei.get("strompreis"), 
        datei.get("ausrichtung"), datei.get("aufstellwinkel"), datei.get("kalkZins"), datei.get("strompreissteigerung"), datei.get("speicher_kWh"), 
        datei.get("dachart"), datei.get("aufstaenderung"), datei.get("dachhaelfte"), 
        datei.get("invest_parameter"), datei.get("betrieb_parameter"), datei.get("zusatzkosten"), datei.get("einspeiseverguetung"), datei.get("absolute_kosten"))
        gewinnkurve_2 = gewinnkurve.tolist()
        ergebnis = [barwert, rendite, gewinnkurve_2, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten]
        return _corsify_actual_response(jsonify(ergebnis))
    else:
        raise Exception('Mein eigener Fehler in /ev')

@app.route("/ms", methods = ["POST", "OPTIONS"])
def ms():
    if request.method == "OPTIONS": # CORS preflight
            return _build_cors_preflight_response()
    elif request.method == "POST": #Actual request following the preflight
        datei = request.get_json()
        [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = berechnung_ms(datei.get("wetterstation"), datei.get("dachart"), datei.get("aufstaenderung"), datei.get("dachhaelfte"), datei.get("strompreis"),
        datei.get("kW"), datei.get("strompreissteigerung"), datei.get("i_teilnehmer"), datei.get("ausrichtung"), datei.get("aufstellwinkel"), datei.get("mieterstromzuschlag"),
        datei.get("kalkZins"), datei.get("rolle"),
        datei.get("invest_parameter"), datei.get("betrieb_parameter"), datei.get("zusatzkosten"), datei.get("einspeiseverguetung"), datei.get("absolute_kosten"))
        gewinnkurve_2 = gewinnkurve.tolist()
        ergebnis = [barwert, rendite, gewinnkurve_2, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten]
        return _corsify_actual_response(jsonify(ergebnis))
    else:
        raise Exception('Mein eigener Fehler in /ev')

@app.route("/gw_ev", methods = ["POST", "OPTIONS"])
def gw_ev():
    if request.method == "OPTIONS": # CORS preflight
            return _build_cors_preflight_response()
    elif request.method == "POST": #Actual request following the preflight
        datei = request.get_json()
        [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = berechnung_gw_ev(datei.get("wetterstation"), datei.get("dachart"), datei.get("aufstaenderung"), datei.get("dachhaelfte"), datei.get("strompreis"),
        datei.get("kW"), datei.get("strompreissteigerung"), datei.get("ausrichtung"), datei.get("aufstellwinkel"),
        datei.get("kalkZins"), datei.get("jahresstromverbrauch"), datei.get("lastprofil"), 
        datei.get("invest_parameter"), datei.get("betrieb_parameter"), datei.get("zusatzkosten"), datei.get("einspeiseverguetung"), 
        datei.get("eigenverbrauchsanteil"), datei.get("lastprofil_verwenden"), datei.get("absolute_kosten"))
        gewinnkurve_2 = gewinnkurve.tolist()
        ergebnis = [barwert, rendite, gewinnkurve_2, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten]
        return _corsify_actual_response(jsonify(ergebnis))
    else:
        raise Exception('Mein eigener Fehler in /ev')

@app.route("/gw_ds", methods = ["POST", "OPTIONS"])
def gw_ds():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST": #Actual request following the preflight
        datei = request.get_json()
        [barwert, rendite, gewinnkurve, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten] = berechnung_gw_ds(datei.get("wetterstation"), datei.get("dachart"), datei.get("aufstaenderung"), datei.get("dachhaelfte"), datei.get("strompreis"), 
        datei.get("kW"), datei.get("strompreissteigerung"), datei.get("ausrichtung"), datei.get("aufstellwinkel"), datei.get("kalkZins"), datei.get("jahresstromverbrauch"), datei.get("rolle"), datei.get("lastprofil"),
        datei.get("invest_parameter"), datei.get("betrieb_parameter"), datei.get("zusatzkosten"), datei.get("einspeiseverguetung"), 
        datei.get("eigenverbrauchsanteil"), datei.get("lastprofil_verwenden"), datei.get("absolute_kosten"))
        gewinnkurve_2 = gewinnkurve.tolist()
        ergebnis = [barwert, rendite, gewinnkurve_2, eigenverbrauchsanteil, autarkiegrad, stromgestehungskosten]
        return _corsify_actual_response(jsonify(ergebnis))
    else:
        raise Exception('Mein eigener Fehler in /ev')

@app.route("/gw_ve", methods = ["POST", "OPTIONS"])
def gw_ve():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST": #Actual request following the preflight
        datei = request.get_json()
        [barwert, rendite, gewinnkurve, stromgestehungskosten] = berechnung_gw_ve(datei.get("wetterstation"), datei.get("dachart"), datei.get("aufstaenderung"), datei.get("dachhaelften"), datei.get("kW"), datei.get("ausrichtung"), datei.get("aufstellwinkel"), datei.get("kalkZins"),
        datei.get("invest_parameter"), datei.get("betrieb_parameter"), datei.get("zusatzkosten"), datei.get("einspeiseverguetung"), datei.get("absolute_kosten"))
        gewinnkurve_2 = gewinnkurve.tolist()
        ergebnis = [barwert, rendite, gewinnkurve_2, stromgestehungskosten]
        return _corsify_actual_response(jsonify(ergebnis))
    else:
        raise Exception('Mein eigener Fehler in /ev')

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    #app.run(port=5002, threaded=True, host="0.0.0.0")
    app.run(port=5002, host="0.0.0.0")