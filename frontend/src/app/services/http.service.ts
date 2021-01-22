import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup } from '@angular/forms';
import { environment } from 'src/environments/environment';

export interface BerechnungsDaten_MS {
    rolle?: string;
    i_teilnehmer?: number;
    mieterstromzuschlag?: number;
    strompreis?: number;
    //Immer gleich
    einspeiseverguetung?: number[];
    zusatzkosten?: number;
    invest_parameter?: number[];
    betrieb_parameter?: number[];
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

    httpPost_ms(form: FormGroup) {
        let data_ms: BerechnungsDaten_MS = {};

        data_ms.einspeiseverguetung = JSON.parse(localStorage.getItem("einspeiseverguetung"));
        data_ms.invest_parameter = JSON.parse(localStorage.getItem("parameter_invest"));
        data_ms.betrieb_parameter = JSON.parse(localStorage.getItem("parameter_betrieb"));
        data_ms.zusatzkosten = JSON.parse(localStorage.getItem("zusatzkosten"));
        data_ms.absolute_kosten = JSON.parse(localStorage.getItem("absolute_kosten"));
        data_ms.wetterstation = localStorage.getItem('wetterstation');
        data_ms.dachart = form.controls["dachart_control"].value;
        data_ms.aufstaenderung = form.controls["aufstaenderung_control"].value;
        data_ms.dachhaelfte = form.controls["dachhaelften_control"].value;
        data_ms.strompreis = form.controls["strompreis_control"].value;
        data_ms.kW = form.controls["leistung_slider_control"].value;
        data_ms.strompreissteigerung = form.controls["strompreissteigerung_control"].value;
        data_ms.i_teilnehmer = form.controls["anzahl_wohneinheiten_control"].value * (form.controls["anteil_wohneinheiten_control"].value / 100)
        data_ms.ausrichtung = form.controls["ausrichtung_slider_control"].value;
        data_ms.aufstellwinkel = form.controls["aufstellwinkel_slider_control"].value;
        data_ms.mieterstromzuschlag = form.controls["mieterstromzuschlag_control"].value;
        data_ms.kalkZins = form.controls["kalk_zins_control"].value;
        data_ms.rolle = form.controls["betreiber_control"].value;
        return this.httpClient.post<any>(this.baseURL+'/ms', data_ms);
    }

}