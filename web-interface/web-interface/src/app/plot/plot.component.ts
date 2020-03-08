import { Component, OnInit } from '@angular/core';
import { ChartType, ChartDataSets } from 'chart.js';
import { Label } from 'ng2-charts';

@Component({
  selector: 'app-plot',
  templateUrl: './plot.component.html',
  styleUrls: ['./plot.component.scss']
})
export class PlotComponent implements OnInit {

  listReglages : any[] = [{Nom:"Eau", Nombre:65},
                          {Nom:"Nutriment", Nombre:30},
                          {Nom:"Luminosité", Nombre:60}
  ];

  public barChartLabels: Label[] = ['Eau', 'Nutriment', 'Luminosité'];
  public barChartType: ChartType = 'bar';
  public barChartLegend = false;
    public chartColors = [
      {
        backgroundColor: ['rgba(0,0,255,0.5)', 'rgba(0,255,0,0.5)', 'rgba(255,0,0,0.5)'],
      }
  ];

  public barChartData: ChartDataSets[] = [
    { data: [65, 30, 55], label: 'Actuel' }
  ];

  constructor() { }

  ngOnInit() {
  }

}
