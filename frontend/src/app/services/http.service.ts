import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup } from '@angular/forms';
import { environment } from 'src/environments/environment';

export interface BerechnungsDaten_EV {
    speicher_kWh?: number;
    //anzahl_personen?: number;
    jahresstromverbrauch?: number;
    strompreis?: number;
    //Immer gleich
    einspeiseverguetung?: number[];
    invest_parameter?: number[];
    betrieb_parameter?: number[];
    zusatzkosten?: number;
    absolute_kosten?: number[];
    kW?: number;
    wetterstation?: string;
    strompreissteigerung?: number;
    kalkZins?: number;
    dachart?: string;
    dachhaelfte?: string;
    aufstaenderung?: string;
    ausrichtung?: number;
    aufstellwinkel?: number;
}

@Injectable({ providedIn: 'root' })
export class HttpService {
    baseURL = environment.baseURL;
    constructor(private httpClient: HttpClient) { }

    httpPost_ev(form: FormGroup) {
        let data_ev: BerechnungsDaten_EV = {};
        data_ev.einspeiseverguetung = JSON.parse(localStorage.getItem("einspeiseverguetung"));
        data_ev.invest_parameter = JSON.parse(localStorage.getItem("parameter_invest"));
        data_ev.betrieb_parameter = JSON.parse(localStorage.getItem("parameter_betrieb"));
        data_ev.zusatzkosten = JSON.parse(localStorage.getItem("zusatzkosten"));
        data_ev.absolute_kosten = JSON.parse(localStorage.getItem("absolute_kosten"));
        data_ev.wetterstation = localStorage.getItem('wetterstation');
        data_ev.kW = form.controls["leistung_slider_control"].value;
        data_ev.speicher_kWh = form.controls["speicher_kWh_control"].value;
        data_ev.jahresstromverbrauch = form.controls["jahresstromverbrauch_control"].value;
        data_ev.strompreis = form.controls["strompreis_control"].value;
        data_ev.strompreissteigerung = form.controls["strompreissteigerung_control"].value;
        data_ev.kalkZins = form.controls["kalk_zins_control"].value;
        data_ev.dachart = form.controls["dachart_control"].value;
        data_ev.dachhaelfte = form.controls["dachhaelften_control"].value;
        data_ev.aufstaenderung = form.controls["aufstaenderung_control"].value;
        data_ev.ausrichtung = form.controls["ausrichtung_slider_control"].value;
        data_ev.aufstellwinkel = form.controls["aufstellwinkel_slider_control"].value;
        return this.httpClient.post<any>(this.baseURL+'/ev', data_ev);
    }

}