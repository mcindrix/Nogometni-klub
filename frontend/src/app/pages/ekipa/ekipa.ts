import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Api } from '../../services/api';
import { Auth } from '../../services/auth';
import { Ekipa as EkipaModel } from '../../models/models';

@Component({
  selector: 'app-ekipa',
  imports: [FormsModule],
  templateUrl: './ekipa.html',
  styleUrl: './ekipa.css',
})
export class Ekipa implements OnInit {
  private api = inject(Api);
  auth = inject(Auth);

  ekipe = signal<EkipaModel[]>([]);
  greska = signal<string | null>(null);
  forma: Partial<EkipaModel> = { Naziv: '', Liga: '' };

  ngOnInit(): void {
    this.ucitaj();
  }

  ucitaj(): void {
    this.api.getEkipe().subscribe((podaci) => this.ekipe.set(podaci));
  }

  dodaj(): void {
    this.greska.set(null);
    this.api.dodajEkipu(this.forma).subscribe({
      next: () => {
        this.forma = { Naziv: '', Liga: '' };
        this.ucitaj();
      },
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom dodavanja ekipe'),
    });
  }

  obrisi(id: number): void {
    this.greska.set(null);
    this.api.obrisiEkipu(id).subscribe({
      next: () => this.ucitaj(),
      error: (err) => this.greska.set(err.error?.detail ?? 'Greška prilikom brisanja'),
    });
  }
}
