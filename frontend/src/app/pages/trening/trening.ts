import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Ekipa, Stadion, Trener, Trening as TreningModel } from '../../models/models';

@Component({
  selector: 'app-trening',
  imports: [FormsModule, DatePipe],
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

  prosli = computed(() =>
    this.treninzi().filter((t) => new Date(t.DatumVrijeme) < new Date()),
  );
  dolazeci = computed(() =>
    this.treninzi()
      .filter((t) => new Date(t.DatumVrijeme) >= new Date())
      .sort((a, b) => new Date(a.DatumVrijeme).getTime() - new Date(b.DatumVrijeme).getTime()),
  );

  ngOnInit(): void {
    this.ucitaj();
    if (!this.auth.igrac()) {
      this.api.getEkipe().subscribe((podaci) => this.ekipe.set(podaci));
      this.api.getTrenere().subscribe((podaci) => this.treneri.set(podaci));
      this.api.getStadione().subscribe((podaci) => this.stadioni.set(podaci));
    }
  }

  ucitaj(): void {
    const izvor = this.auth.igrac() ? this.api.getMojiTreninzi() : this.api.getTreninge();
    izvor.subscribe((podaci) => this.treninzi.set(podaci));
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
