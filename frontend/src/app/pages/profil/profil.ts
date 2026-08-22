import { Component, OnInit, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Ekipa, Igrac, Trener, Trening, Utakmica } from '../../models/models';

@Component({
  selector: 'app-profil',
  imports: [DatePipe],
  templateUrl: './profil.html',
  styleUrl: './profil.css',
})
export class Profil implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  igrac = signal<Igrac | null>(null);
  trener = signal<Trener | null>(null);
  ekipe = signal<Ekipa[]>([]);
  utakmice = signal<Utakmica[]>([]);
  treninzi = signal<Trening[]>([]);
  greska = signal<string | null>(null);

  ngOnInit(): void {
    if (this.auth.igrac()) {
      this.api.getMojIgrac().subscribe({
        next: (podaci) => {
          this.igrac.set(podaci);
          this.ekipe.set(podaci.ekipa ? [podaci.ekipa] : []);
        },
        error: () => this.greska.set('Ne mogu dohvatiti profil.'),
      });
    } else if (this.auth.trener()) {
      this.api.getMojTrener().subscribe({
        next: (podaci) => this.trener.set(podaci),
        error: () => this.greska.set('Ne mogu dohvatiti profil.'),
      });
      this.api.getMojeEkipeTrenera().subscribe((podaci) => this.ekipe.set(podaci));
    }

    this.api.getMojeUtakmice().subscribe((podaci) => this.utakmice.set(podaci));
    this.api.getMojiTreninzi().subscribe((podaci) => this.treninzi.set(podaci));
  }
}
