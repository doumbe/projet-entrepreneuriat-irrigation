import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {MainComponent} from './main/main.component';
import { ListPlotsComponent } from './list-plots/list-plots.component';
import { PlotComponent } from './plot/plot.component';

const routes: Routes = [
  {path:'',redirectTo: '/home', pathMatch: 'full'},
  {path: 'home', component : MainComponent},
  {path: 'plot', component : PlotComponent},
  {path: 'plots', component : ListPlotsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
