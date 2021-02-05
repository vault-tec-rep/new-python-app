import { Component, OnInit } from '@angular/core';
import { EChartsOption } from 'echarts';

@Component({
  selector: 'app-durchschnittstag-graph',
  templateUrl: './durchschnittstag-graph.component.html',
  styleUrls: ['./durchschnittstag-graph.component.css']
})
export class DurchschnittstagGraphComponent implements OnInit {
  chartInstance;
  
  chartOption: EChartsOption = {
    xAxis: {
      type: 'value',
      name: 'Minuten',
      min: 0, 
      max: 1440,
    },
    yAxis: {
      type: 'value',
      name: 'kW',
    },
    series: [
      {
        data: [],
        type: 'line',
        lineStyle: {color: '#76B900' }
      },
      {
        data: [],
        type: 'line',
        lineStyle: {color: '#000000' }
      }
    ],
  };

  constructor() { }

  ngOnInit(): void {
  }

  aktualisiere_chart(wertepaare_pv, wertepaare_last, laenge) {
    let option = this.chartInstance.getOption();

    option.xAxis = {
      type: 'value',
      name: 'Minuten',
      min: 0, 
      max: laenge,
    }

    option.series[0] = {
      data: wertepaare_pv,
    };
    option.series[1] = {
      data: wertepaare_last,
    };
    this.chartInstance.setOption(option);

  }
  onChartInit(chart) {
    this.chartInstance = chart;
  }
}
