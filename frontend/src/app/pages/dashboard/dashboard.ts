import { Component } from '@angular/core';
import { Header } from '../../components/header/header';
import { NavbarComponent } from '../../components/navbar/navbar';

@Component({
  selector: 'app-dashboard',
  imports: [NavbarComponent, Header],
  templateUrl: './dashboard.html',
})
export class Dashboard {}
