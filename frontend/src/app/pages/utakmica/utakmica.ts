import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Ekipa, Stadion, Utakmica as UtakmicaModel } from '../../models/models';

@Component({
  selector: 'app-utakmica',
  imports: [FormsModule, DatePipe],
  templateUrl: './utakmica.html',
  styleUrl: './utakmica.css',
})
export class Utakmica implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  utakmice = signal<UtakmicaModel[]>([]);
  ekipe = signal<Ekipa[]>([]);
  stadioni = signal<Stadion[]>([]);
  greska = signal<string | null>(null);
  forma: Partial<UtakmicaModel> = {
    EkipaID: undefined,
    Protivnik: '',
    StadionID: undefined,
    DatumVrijeme: '',
    RezultatNas: null,
    RezultatProtivnik: null,
  };

  odigrane = computed(() =>
    this.utakmice().filter((u) => new Date(u.DatumVrijeme) < new Date()),
  );
  nadolazece = computed(() =>
    this.utakmice()
      .filter((u) => new Date(u.DatumVrijeme) >= new Date())
      .sort((a, b) => new Date(a.DatumVrijeme).getTime() - new Date(b.DatumVrijeme).getTime()),
  );

  ngOnInit(): void {
    this.ucitaj();
    if (!this.auth.igrac()) {
      this.api.getEkipe().subscribe((podaci) => this.ekipe.set(podaci));
      this.api.getStadione().subscribe((podaci) => this.stadioni.set(podaci));
    }
  }

  ucitaj(): void {
    const izvor = this.auth.igrac() ? this.api.getMojeUtakmice() : this.api.getUtakmice();
    izvor.subscribe((podaci) => this.utakmice.set(podaci));
  }

  dodaj(): void {
    this.greska.set(null);
    this.api.dodajUtakmicu(this.forma).subscribe({
      next: () => {
        this.forma = {
          EkipaID: undefined,
          Protivnik: '',
          StadionID: undefined,
          DatumVrijeme: '',
          RezultatNas: null,
          RezultatProtivnik: null,
        };
        this.ucitaj();
      },
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom dodavanja utakmice'),
    });
  }

  obrisi(id: number): void {
    this.greska.set(null);
    this.api.obrisiUtakmicu(id).subscribe({
      next: () => this.ucitaj(),
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom brisanja'),
    });
  }
}
