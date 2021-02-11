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
        let einspeiseverguetungVektor: number[] = [0, 0, 0];
        let schule: number;
        let geschäftsmodell: number;
        //Zusammenstellen der Vektoren
        einspeiseverguetungVektor[0] = form.controls["Einspeisung_A_control"].value;
        einspeiseverguetungVektor[1] = form.controls["Einspeisung_B_control"].value;
        einspeiseverguetungVektor[2] = form.controls["Einspeisung_C_control"].value;

        if(form.controls["lastprofil_control"].value == 0) {
            schule = 1;
        }
        else {
            schule = 0;
        }

        if(form.controls["lastprofil_control"].value == 1) {
            geschäftsmodell = 1;
        }
        else {
            geschäftsmodell = 2;
        }

        //Füllen des leeren Interfaces mit den relevanten Daten
        data.einspeiseverguetungVektor = einspeiseverguetungVektor;
        data.strompreis = form.controls["strompreis_control"].value;
        data.kW = form.controls["leistung_slider_control"].value;
        data.strompreissteigerung = form.controls["strompreissteigerung_control"].value;
        data.kalkZins = form.controls["kalk_zins_control"].value;
        data.lastprofilNummer = form.controls["lastprofil_control"].value;
        data.jahresstromverbrauch = form.controls["jahresstromverbrauch_control"].value;
        data.i_teilnehmer = Math.ceil(form.controls["wohneinheiten_control"].value * (form.controls["teilnahme_prozent_control"].value / 100));
        data.spez_kosten_pv = form.controls["spez_kosten_pv_control"].value;
        data.schule = schule;
        data.geschäftsmodell = geschäftsmodell;

        return this.httpClient.post<any>(this.baseURL+'/main', data);
    }

}