import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Pozicija as PozicijaModel } from '../../models/models';

@Component({
  selector: 'app-pozicija',
  imports: [FormsModule],
  templateUrl: './pozicija.html',
  styleUrl: './pozicija.css',
})
export class Pozicija implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  pozicije = signal<PozicijaModel[]>([]);
  greska = signal<string | null>(null);
  forma: Partial<PozicijaModel> = { Naziv: '', Opis: '' };

  ngOnInit(): void {
    this.ucitaj();
  }

  ucitaj(): void {
    this.api.getPozicije().subscribe((podaci) => this.pozicije.set(podaci));
  }

  dodaj(): void {
    this.greska.set(null);
    this.api.dodajPoziciju(this.forma).subscribe({
      next: () => {
        this.forma = { Naziv: '', Opis: '' };
        this.ucitaj();
      },
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom dodavanja pozicije'),
    });
  }

  obrisi(id: number): void {
    this.greska.set(null);
    this.api.obrisiPoziciju(id).subscribe({
      next: () => this.ucitaj(),
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom brisanja'),
    });
  }
}
