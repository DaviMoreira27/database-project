import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Dashboard } from './pages/dashboard/dashboard';
import { Managers } from './pages/managers/managers';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'login' },
  { path: 'login', component: Login, title: 'Login' },
  { path: 'dashboard', component: Dashboard, title: 'Dashboard' },
  { path: 'managers', component: Managers, title: 'Gerentes' },
];
