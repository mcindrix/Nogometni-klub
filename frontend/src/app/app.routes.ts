import { inject } from '@angular/core';
import { Routes } from '@angular/router';

import { Auth } from './services/auth';
import { authGuard } from './services/auth-guard';

const pocetnaZaUlogu = () => (inject(Auth).admin() ? 'dashboard' : 'profil');

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then((m) => m.Login),
  },
  {
    path: '',
    canActivateChild: [authGuard],
    children: [
      { path: '', pathMatch: 'full', redirectTo: pocetnaZaUlogu },
      {
        path: 'dashboard',
        loadComponent: () => import('./pages/dashboard/dashboard').then((m) => m.Dashboard),
      },
      {
        path: 'profil',
        loadComponent: () => import('./pages/profil/profil').then((m) => m.Profil),
        data: { dozvoljeneUloge: ['Igrac', 'Trener'] },
      },
      {
        path: 'stadioni',
        loadComponent: () => import('./pages/stadion/stadion').then((m) => m.Stadion),
        data: { dozvoljeneUloge: ['Admin'] },
      },
      {
        path: 'treneri',
        loadComponent: () => import('./pages/trener/trener').then((m) => m.Trener),
        data: { dozvoljeneUloge: ['Admin'] },
      },
      {
        path: 'ekipe',
        loadComponent: () => import('./pages/ekipa/ekipa').then((m) => m.Ekipa),
        data: { dozvoljeneUloge: ['Admin'] },
      },
      {
        path: 'igraci',
        loadComponent: () => import('./pages/igrac/igrac').then((m) => m.Igrac),
        data: { dozvoljeneUloge: ['Admin', 'Trener'] },
      },
      {
        path: 'clanarine',
        loadComponent: () => import('./pages/clanarina/clanarina').then((m) => m.Clanarina),
        data: { dozvoljeneUloge: ['Admin', 'Trener'] },
      },
      {
        path: 'utakmice',
        loadComponent: () => import('./pages/utakmica/utakmica').then((m) => m.Utakmica),
      },
      {
        path: 'treninzi',
        loadComponent: () => import('./pages/trening/trening').then((m) => m.Trening),
      },
      { path: '**', redirectTo: pocetnaZaUlogu },
    ],
  },
];
