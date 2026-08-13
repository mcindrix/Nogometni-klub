import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Ekipa, Igrac as IgracModel, Pozicija } from '../../models/models';

@Component({
  selector: 'app-igrac',
  imports: [FormsModule],
  templateUrl: './igrac.html',
  styleUrl: './igrac.css',
})
export class Igrac implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  igraci = signal<IgracModel[]>([]);
  pozicije = signal<Pozicija[]>([]);
  ekipe = signal<Ekipa[]>([]);
  greska = signal<string | null>(null);
  forma: Partial<IgracModel> = { Ime: '', Prezime: '', DatumRodjenja: null, PozicijaID: undefined, EkipaID: null };

  ngOnInit(): void {
    this.ucitaj();
    this.api.getPozicije().subscribe((podaci) => this.pozicije.set(podaci));
    this.api.getEkipe().subscribe((podaci) => this.ekipe.set(podaci));
  }

  ucitaj(): void {
    this.api.getIgrace().subscribe((podaci) => this.igraci.set(podaci));
  }

  dodaj(): void {
    this.greska.set(null);
    this.api.dodajIgraca(this.forma).subscribe({
      next: () => {
        this.forma = { Ime: '', Prezime: '', DatumRodjenja: null, PozicijaID: undefined, EkipaID: null };
        this.ucitaj();
      },
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom dodavanja igrača'),
    });
  }

  obrisi(id: number): void {
    this.greska.set(null);
    this.api.obrisiIgraca(id).subscribe({
      next: () => this.ucitaj(),
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom brisanja'),
    });
  }
}
