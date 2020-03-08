import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatSort, MatTableDataSource } from '@angular/material';

export interface table {
  number: string;
  name: string;
  color: string;
}
const rows: table[] = [
  {number:"1",name:"Plan de Tomates Nord", color:"green"},
  {number:"2",name:"Plan de Maïs Sud", color:"orange"},
  {number:"3",name:"Plan de Carotte Ouest", color:"red"},
];
@Component({
  selector: 'app-list-plots',
  templateUrl: './list-plots.component.html',
  styleUrls: ['./list-plots.component.scss']
})
export class ListPlotsComponent implements OnInit {

  @ViewChild(MatPaginator,{static: false}) paginator: MatPaginator;
  @ViewChild(MatSort,{static: false}) sort: MatSort;

  displayedColumns: string[] = ['number','name','color'];
  dataSource: MatTableDataSource<table>;
  constructor() {
    this.dataSource = new MatTableDataSource(rows);
  }

  ngOnInit() {
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }
}
