//angular components
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
//angular material
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button'; 
import { MatSliderModule } from '@angular/material/slider'; 
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
//main component
import { MainComponent } from './main/main.component';
//echarts
import { NgxEchartsModule } from 'ngx-echarts';
import * as echarts from 'echarts';
//chart components

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
  ],
  imports: [
    //angular modules
    BrowserModule,
    NgbModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    //material Module
    MatSlideToggleModule,
    MatInputModule,
    MatFormFieldModule,
    MatTabsModule,
    MatToolbarModule,
    MatRadioModule,
    MatButtonModule,
    MatSliderModule,
    MatTableModule,
    MatIconModule,
    MatSelectModule,
    //echarts
    NgxEchartsModule.forRoot({echarts}),


  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
