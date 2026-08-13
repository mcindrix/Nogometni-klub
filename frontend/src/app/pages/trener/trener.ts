import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Trener as TrenerModel } from '../../models/models';

@Component({
  selector: 'app-trener',
  imports: [FormsModule],
  templateUrl: './trener.html',
  styleUrl: './trener.css',
})
export class Trener implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  treneri = signal<TrenerModel[]>([]);
  greska = signal<string | null>(null);
  forma: Partial<TrenerModel> = { Ime: '', Prezime: '', Licenca: '', DatumRodjenja: null };

  ngOnInit(): void {
    this.ucitaj();
  }

  ucitaj(): void {
    this.api.getTrenere().subscribe((podaci) => this.treneri.set(podaci));
  }

  dodaj(): void {
    this.greska.set(null);
    this.api.dodajTrenera(this.forma).subscribe({
      next: () => {
        this.forma = { Ime: '', Prezime: '', Licenca: '', DatumRodjenja: null };
        this.ucitaj();
      },
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom dodavanja trenera'),
    });
  }

  obrisi(id: number): void {
    this.greska.set(null);
    this.api.obrisiTrenera(id).subscribe({
      next: () => this.ucitaj(),
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom brisanja'),
    });
  }
}
