import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup } from '@angular/forms';
import { environment } from 'src/environments/environment';

export interface BerechnungsDaten {
    strompreis?: number;
    kW?: number;
    strompreissteigerung?: number;
    kalkZins?: number;
    jahresstromverbrauch?: number;
    lastprofilNummer?: number;
    einspeiseverguetungVektor?: number[];
    i_teilnehmer?: number;
    spez_kosten_pv?: number;
    geschäftsmodell?: number;
    schule?: number;

}


@Injectable({ providedIn: 'root' })
export class HttpService {
    baseURL = environment.baseURL;
    constructor(private httpClient: HttpClient) { }

    httpPost(form: FormGroup) {
        let data: BerechnungsDaten = {};

        data.strompreis = form.controls["strompreis_control"].value;
        data.kW = form.controls["leistung_slider_control"].value;
        data.strompreissteigerung = form.controls["strompreissteigerung_control"].value;
        data.kalkZins = form.controls["kalk_zins_control"].value;
        data.jahresstromverbrauch = form.controls["jahresstromverbrauch_control"].value;
        data.lastprofilNummer = form.controls["lastprofilNummer_control"].value;
        data.einspeiseverguetungVektor = form.controls["einspeiseverguetungVektor"].value;
        data.i_teilnehmer = Math.ceil(form.controls["wohneinheiten_control"].value * (form.controls["teilnahme_prozent_control"].value / 100));
        data.spez_kosten_pv = form.controls["spez_kosten_pv_control"].value;
        data.geschäftsmodell = JSON.parse(localStorage.getItem("geschäftsmodell"));
        data.schule = JSON.parse(localStorage.getItem("schule"));

        return this.httpClient.post<any>(this.baseURL+'/main', data);
    }

}