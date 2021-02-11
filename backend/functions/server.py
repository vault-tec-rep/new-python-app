from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
#Für Deployment
#from Berechnungsfunktionen import berechnung
#Für ng-serve testen
from Berechnungsfunktionen_lokal import berechnung
app = Flask(__name__)
CORS(app)


@app.route("/main", methods = ["POST", "OPTIONS"])
def main_berechnung():
    if request.method == "OPTIONS": # CORS preflight
            return _build_cors_preflight_response()
    elif request.method == "POST": #Actual request following the preflight
        datei = request.get_json()
        [barwert_mieterstrom, barwert_eigenverbrauch, eigenverbrauchsanteil, autarkiegrad, durchschnittstag_pv, durchschnittstag_last] = berechnung(datei.get("strompreis"), datei.get("kW"), datei.get("strompreissteigerung"), 
            datei.get("kalkZins"), datei.get("jahresstromverbrauch"), datei.get("lastprofilNummer"), datei.get("einspeiseverguetungVektor"), datei.get("i_teilnehmer"),
            datei.get("spez_kosten_pv"), datei.get("geschäftsmodell"), datei.get("schule"))

        durchschnittstag_pv = durchschnittstag_pv.tolist()
        durchschnittstag_last = durchschnittstag_last.tolist()
        ergebnis = [barwert_mieterstrom, barwert_eigenverbrauch, eigenverbrauchsanteil, autarkiegrad, durchschnittstag_pv, durchschnittstag_last]
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