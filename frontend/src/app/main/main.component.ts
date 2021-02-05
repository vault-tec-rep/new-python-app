//Notwendige Imports anderer Komponenten
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { DurchschnittstagGraphComponent } from '../charts/durchschnittstag-graph/durchschnittstag-graph.component';
import { HttpService } from '../services/http.service';
import { CustomIconService } from '../services/icon.service';


//Definition des Lastprofils (Besteht aus einem Index, sowie einem String, der das Lastprofil beschreibt)
interface Lastprofil {
  value: number;
  viewValue: string;
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

  @ViewChild(DurchschnittstagGraphComponent) chart_durchschnittsgraph: DurchschnittstagGraphComponent;

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
      'jahresstromverbrauch_control': new FormControl(3000, [Validators.required, Validators.min(1), Validators.max(100000)]),
      'dachgröße_control': new FormControl(20, [Validators.required, Validators.min(1), Validators.max(10000)]), 
      'strompreis_slider_control': new FormControl(28, Validators.required),
      'lastprofil_control': new FormControl(2, Validators.required),
      'strompreissteigerung_control': new FormControl(2, [Validators.required, Validators.min(0), Validators.max(200)]),
      'kalk_zins_control': new FormControl(2, [Validators.required, Validators.min(0), Validators.max(200)]),
      'spez_kosten_pv_control': new FormControl(1000, [Validators.required, Validators.min(0), Validators.max(10000)]),
      'Einspeisung_A': new FormControl(9.30, [Validators.required, Validators.min(0), Validators.max(50)]),
      'Einspeisung_B': new FormControl(9.05, [Validators.required, Validators.min(0), Validators.max(50)]),
      'Einspeisung_C': new FormControl(7.19, [Validators.required, Validators.min(0), Validators.max(50)]),
      'wohneinheiten_control': new FormControl(10, [Validators.required, Validators.min(1), Validators.max(20)]),
      'teilnahme_prozent_control': new FormControl(50, [Validators.required, Validators.min(1), Validators.max(100)])
    });
  }



  //Methode, die die Daten aus dem Formular an das Backend sendet. Geschieht über eine Funktion aus dem selbst erstellten HTTP-Service
  berechnungSenden() {
    //Über subscribe wird auf die Antwort des Backends gewartet. Die Antwort wird in result gespeichert und anschließend der Code nach dem Pfeil ausgeführt
    this.httpService.httpPost(this.berechnungForm_main).subscribe(result => {
      //Entpacken der Antwort

      //Aktualisieren der Visualisierung
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

  onErweiterteEinstellungenChange() {
    this.erweiterte_einstellungen_boolean = !this.erweiterte_einstellungen_boolean;
  }
}
