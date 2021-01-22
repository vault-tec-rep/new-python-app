import { Injectable } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Injectable({ providedIn: 'root' })
export class CustomIconService {
    constructor(private matIconRegistry: MatIconRegistry,
        private domSanitizer: DomSanitizer) { }

    init() {
        //sun
        this.matIconRegistry.addSvgIcon('custom-sun',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../../assets/custom-icons/sun.svg'));
        //water drop
        this.matIconRegistry.addSvgIcon('custom-water',
        this.domSanitizer.bypassSecurityTrustResourceUrl('../../assets/custom-icons/water-drop.svg'));
        //battery
        this.matIconRegistry.addSvgIcon('custom-battery',
        this.domSanitizer.bypassSecurityTrustResourceUrl('../../assets/custom-icons/battery.svg'));
        //cog
        this.matIconRegistry.addSvgIcon('custom-cog',
        this.domSanitizer.bypassSecurityTrustResourceUrl('../../assets/custom-icons/cog.svg'));
        //energy-bulb
        this.matIconRegistry.addSvgIcon('custom-energy',
        this.domSanitizer.bypassSecurityTrustResourceUrl('../../assets/custom-icons/energy-bulb.svg'));
        //euro
        this.matIconRegistry.addSvgIcon('custom-euro',
        this.domSanitizer.bypassSecurityTrustResourceUrl('../../assets/custom-icons/euro.svg'));
        //people
        this.matIconRegistry.addSvgIcon('custom-people',
        this.domSanitizer.bypassSecurityTrustResourceUrl('../../assets/custom-icons/people.svg'));
        //apartment
        this.matIconRegistry.addSvgIcon('custom-apartement',
        this.domSanitizer.bypassSecurityTrustResourceUrl('../../assets/custom-icons/apartement.svg'));

    }


}