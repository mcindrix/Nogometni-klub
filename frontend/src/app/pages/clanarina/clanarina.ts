import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CurrencyPipe } from '@angular/common';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Clanarina as ClanarinaModel, Igrac } from '../../models/models';

@Component({
  selector: 'app-clanarina',
  imports: [FormsModule, CurrencyPipe],
  templateUrl: './clanarina.html',
  styleUrl: './clanarina.css',
})
export class Clanarina implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  clanarine = signal<ClanarinaModel[]>([]);
  igraci = signal<Igrac[]>([]);
  greska = signal<string | null>(null);
  forma: Partial<ClanarinaModel> = { IgracID: undefined, Iznos: undefined, DatumUplate: '', Razdoblje: '' };

  ngOnInit(): void {
    this.ucitaj();
    this.api.getIgrace().subscribe((podaci) => this.igraci.set(podaci));
  }

  ucitaj(): void {
    this.api.getClanarine().subscribe((podaci) => this.clanarine.set(podaci));
  }

  dodaj(): void {
    this.greska.set(null);
    this.api.dodajClanarinu(this.forma).subscribe({
      next: () => {
        this.forma = { IgracID: undefined, Iznos: undefined, DatumUplate: '', Razdoblje: '' };
        this.ucitaj();
      },
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom dodavanja članarine'),
    });
  }

  obrisi(id: number): void {
    this.greska.set(null);
    this.api.obrisiClanarinu(id).subscribe({
      next: () => this.ucitaj(),
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom brisanja'),
    });
  }
}
