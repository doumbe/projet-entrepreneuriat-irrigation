import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {

  listButton=[]
  listColor=["Green","Green","Green","Green","Orange","Red","Grey"];
 
  constructor() { }

  ngOnInit() {
    this.creatList();
  }
  creatList(){
    for (let index = 0; index < 81; index++) {
      this.listButton.push({
        number: index,
        color :  this.listColor[Math.floor(Math.random() * this.listColor.length)]
      });
      
    }
  }
}
