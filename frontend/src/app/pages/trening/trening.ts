import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Ekipa, Stadion, Trener, Trening as TreningModel } from '../../models/models';

@Component({
  selector: 'app-trening',
  imports: [FormsModule],
  templateUrl: './trening.html',
  styleUrl: './trening.css',
})
export class Trening implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  treninzi = signal<TreningModel[]>([]);
  ekipe = signal<Ekipa[]>([]);
  treneri = signal<Trener[]>([]);
  stadioni = signal<Stadion[]>([]);
  greska = signal<string | null>(null);
  forma: Partial<TreningModel> = {
    EkipaID: undefined,
    TrenerID: undefined,
    StadionID: null,
    DatumVrijeme: '',
    Trajanje: null,
  };

  ngOnInit(): void {
    this.ucitaj();
    this.api.getEkipe().subscribe((podaci) => this.ekipe.set(podaci));
    this.api.getTrenere().subscribe((podaci) => this.treneri.set(podaci));
    this.api.getStadione().subscribe((podaci) => this.stadioni.set(podaci));
  }

  ucitaj(): void {
    this.api.getTreninge().subscribe((podaci) => this.treninzi.set(podaci));
  }

  dodaj(): void {
    this.greska.set(null);
    this.api.dodajTrening(this.forma).subscribe({
      next: () => {
        this.forma = { EkipaID: undefined, TrenerID: undefined, StadionID: null, DatumVrijeme: '', Trajanje: null };
        this.ucitaj();
      },
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom dodavanja treninga'),
    });
  }

  obrisi(id: number): void {
    this.greska.set(null);
    this.api.obrisiTrening(id).subscribe({
      next: () => this.ucitaj(),
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom brisanja'),
    });
  }
}
