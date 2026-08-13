import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Stadion as StadionModel } from '../../models/models';

@Component({
  selector: 'app-stadion',
  imports: [FormsModule],
  templateUrl: './stadion.html',
  styleUrl: './stadion.css',
})
export class Stadion implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  stadioni = signal<StadionModel[]>([]);
  greska = signal<string | null>(null);
  forma: Partial<StadionModel> = { Naziv: '', Grad: '', Kapacitet: null };

  ngOnInit(): void {
    this.ucitaj();
  }

  ucitaj(): void {
    this.api.getStadione().subscribe((podaci) => this.stadioni.set(podaci));
  }

  dodaj(): void {
    this.greska.set(null);
    this.api.dodajStadion(this.forma).subscribe({
      next: () => {
        this.forma = { Naziv: '', Grad: '', Kapacitet: null };
        this.ucitaj();
      },
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom dodavanja stadiona'),
    });
  }

  obrisi(id: number): void {
    this.greska.set(null);
    this.api.obrisiStadion(id).subscribe({
      next: () => this.ucitaj(),
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom brisanja'),
    });
  }
}
