//Notwendige Imports anderer Komponenten
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { DurchschnittstagGraphComponent } from '../charts/durchschnittstag-graph/durchschnittstag-graph.component';
import { HttpService } from '../services/http.service';
import { CustomIconService } from '../services/icon.service';
import * as XLSX from 'xlsx';
import { MatTable } from '@angular/material/table';


//Definition des Lastprofils (Besteht aus einem Index, sowie einem String, der das Lastprofil beschreibt)
interface Lastprofil {
  value: number;
  viewValue: string;
}

//Daten für die Tabelle
export interface Ergebnis_Daten {
  kategorie?: string;
  ergebnis?: any;
}

//Deklaration der Main Component
@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})

//Deklaration der Main Component mit einer OnInit Methode (Wird beim Erstellen der Component ausgeführt)
export class MainComponent implements OnInit {
  berechnungForm_main: FormGroup; //Deklaration des Formulars, in das später die Werte eingetragen werden
  erweiterte_einstellungen_boolean: boolean = false;
  mehrfamilienhaus_boolean: boolean = false;
  schule_number_boolean: number = 0;

  //Ergebnisse
  barwert_mieterstrom: number;
  barwert_eigenverbrauch: number;
  eigenverbrauchsanteil: number;
  autarkiegrad: number;
  durchschnittstag_pv: number[];
  durchschnittstag_last: number[];
  vermiedener_netzbezug: number;
  stromkosteneinsparung: number;
  co2_einsparung: number;
  //Daten für die Ergebnistabelle
  displayedColumns: string[] = ['kategorie', 'ergebnis'];
  ELEMENT_DATA: Ergebnis_Daten[] = [
    {kategorie: 'Autarkiegrad in %', ergebnis: 0}, 
    {kategorie: 'Eigenverbrauchsanteil in %', ergebnis: 0}, 
    {kategorie: 'Vermiedener Netzbezug in kWh pro Jahr', ergebnis: 0}, 
    {kategorie: 'Stromkosteneinsparung in Euro pro Jahr', ergebnis: 0}, 
    {kategorie: 'CO2-Einsparung in kg pro Jahr', ergebnis: 0},
    {kategorie: 'Armortisation der Investition', ergebnis: 'Ja/Nein'}
  ];

  table_data = this.ELEMENT_DATA;

  @ViewChild(DurchschnittstagGraphComponent) chart_durchschnittsgraph: DurchschnittstagGraphComponent;
  @ViewChild(MatTable) table: MatTable<any>;

  //Lastprofil
  lastprofil_auswahl: Lastprofil[] = [
    { value: 0, viewValue: 'Schule'},
    { value: 1, viewValue: 'Mehrfamilienhaus'},
    { value: 2, viewValue: 'allgemeines Gewerbe' },
    { value: 3, viewValue: 'Gewerbe werktags 8-18 Uhr' },
    { value: 4, viewValue: 'Gewerbe mit starkem Verbrauch in den Abendstunden' },
    { value: 5, viewValue: 'Gewerbe durchlaufend' },
    { value: 6, viewValue: 'Gewerbe Laden/Friseur' },
    { value: 7, viewValue: 'Gewerbe Bäckerei mit Backstube' },
    { value: 8, viewValue: 'Gewerbe Wochenendbetrieb' },
  ]

  //Integration der beiden services über den constructor
  constructor(
    private httpService: HttpService, 
    private customIconService: CustomIconService) {
    this.customIconService.init();
  }

  //OnInit Methode.
  ngOnInit(): void {
    //Initialisierung des Formulars. Hier werden die jeweiligen Frontendkomponenten in das Formular eingetragen
    this.berechnungForm_main = new FormGroup({
      'leistung_slider_control': new FormControl(10, Validators.required),
      'jahresstromverbrauch_control': new FormControl(3000, [Validators.required, Validators.min(1), Validators.max(1000000)]),
      'dachgröße_control': new FormControl(20, [Validators.required, Validators.min(1), Validators.max(10000)]), 
      'strompreis_control': new FormControl(28, Validators.required),
      'lastprofil_control': new FormControl(2, Validators.required),
      'strompreissteigerung_control': new FormControl(2, [Validators.required, Validators.min(0), Validators.max(200)]),
      'kalk_zins_control': new FormControl(2, [Validators.required, Validators.min(0), Validators.max(200)]),
      'spez_kosten_pv_control': new FormControl(1000, [Validators.required, Validators.min(0), Validators.max(10000)]),
      'Einspeisung_A_control': new FormControl(9.30, [Validators.required, Validators.min(0), Validators.max(50)]),
      'Einspeisung_B_control': new FormControl(9.05, [Validators.required, Validators.min(0), Validators.max(50)]),
      'Einspeisung_C_control': new FormControl(7.19, [Validators.required, Validators.min(0), Validators.max(50)]),
      'wohneinheiten_control': new FormControl(10, [Validators.required, Validators.min(1), Validators.max(20)]),
      'teilnahme_prozent_control': new FormControl(50, [Validators.required, Validators.min(1), Validators.max(100)])
    });
    localStorage.setItem("schule", JSON.stringify(0));
    localStorage.setItem("geschäftsmodell", JSON.stringify(2));
  }

  //Methode, die die Daten aus dem Formular an das Backend sendet. Geschieht über eine Funktion aus dem selbst erstellten HTTP-Service
  berechnungSenden() {
    //Über subscribe wird auf die Antwort des Backends gewartet. Die Antwort wird in result gespeichert und anschließend der Code nach dem Pfeil ausgeführt
    this.httpService.httpPost(this.berechnungForm_main).subscribe(result => {
      let armortisation_string: string;
      //Entpacken der Antwort
      this.barwert_mieterstrom = result[0];
      this.barwert_eigenverbrauch = result[1];
      this.eigenverbrauchsanteil = result[2];
      this.autarkiegrad = result[3];
      this.durchschnittstag_pv = result[4];
      this.durchschnittstag_last = result[5];
      this.vermiedener_netzbezug = result[6];
      this.stromkosteneinsparung = result[7];
      this.co2_einsparung = result[8];
      //Aktualisieren der Visualisierung
      this.chart_durchschnittstag_aktualisieren(this.durchschnittstag_pv, this.durchschnittstag_last);
      //Prüfen ob Armortisation vorhanden
      if (this.mehrfamilienhaus_boolean == true) {
        if (this.barwert_mieterstrom > 0) {
          armortisation_string= 'Ja';
        }
        else {
          armortisation_string = 'Nein';
        }
      }
      else {
        if (this.barwert_eigenverbrauch > 0) {
          armortisation_string = 'Ja';
        }
        else {
          armortisation_string = 'Nein';
        }
      }

      //Vorbereiten der Daten, die in der Tabelle angezeigt werden sollen
      this.ELEMENT_DATA = [
        {kategorie: 'Autarkiegrad in %', ergebnis: this.autarkiegrad}, 
        {kategorie: 'Eigenverbrauchsanteil in %', ergebnis: this.eigenverbrauchsanteil}, 
        {kategorie: 'Vermiedener Netzbezug in kWh pro Jahr', ergebnis: this.vermiedener_netzbezug}, 
        {kategorie: 'Stromkosteneinsparung in Euro pro Jahr', ergebnis: this.stromkosteneinsparung}, 
        {kategorie: 'CO2-Einsparung in kg pro Jahr', ergebnis: this.co2_einsparung},
        {kategorie: 'Armortisation der Investition', ergebnis: armortisation_string}
      ];
      //Aufruf der Funktion, die die Tabelle aktualisiert
      this.ergebnis_werte_aktualisieren(this.ELEMENT_DATA);
    })
  }

  lastprofil_change(value: number) {
    if (value == 1) {
      this.mehrfamilienhaus_boolean = true;
    }
    else {
      this.mehrfamilienhaus_boolean = false;
    }
  }

  dachgroesse_change() {
    let dachgröße_wert: number;
    let ungerundeter_wert: number;

    //Berechnung
    ungerundeter_wert = this.berechnungForm_main.controls["dachgröße_control"].value / 6.5;
    dachgröße_wert = Math.ceil(ungerundeter_wert);
    this.berechnungForm_main.controls["leistung_slider_control"].setValue(dachgröße_wert);
  }

  chart_durchschnittstag_aktualisieren(y_pv: Array<number>, y_last: Array<number>) {
    let x_werte: number = 0;
    let wertepaare_pv: Array<number[]> = [];
    let wertepaare_last: Array<number[]> = [];


    while (x_werte < y_last.length) {
      wertepaare_pv[x_werte] = [x_werte, y_pv[x_werte]];
      wertepaare_last[x_werte] = [x_werte, y_last[x_werte]];
      x_werte++;
    }
    this.chart_durchschnittsgraph.aktualisiere_chart(wertepaare_pv, wertepaare_last, y_last.length);
  }

  ergebnis_werte_aktualisieren(table_data_neu: Ergebnis_Daten[]) {
    //Zuweisen der neuen Daten als Grundlage für die Tabelle
    this.table_data = table_data_neu;
    //Neues Rendern der Tabelle, damit die Änderung sichtbar wird. 
    this.table.renderRows();
  }

  onErweiterteEinstellungenChange() {
    this.erweiterte_einstellungen_boolean = !this.erweiterte_einstellungen_boolean;
  }
}
