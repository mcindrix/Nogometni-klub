import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';

import { PrijavaOdgovor } from '../models/models';

const BASE_URL = 'http://localhost:8000/api';
const STORAGE_KEY = 'nogometni_klub_auth';

interface SpremljenaPrijava {
  token: string;
  korisnickoIme: string;
  uloga: string;
}

@Injectable({
  providedIn:'root'
})
export class Auth {
  private http = inject(HttpClient);

  private spremljeno = this.procitajIzStorage();
  token = signal<string | null>(this.spremljeno?.token ?? null);
  korisnickoIme = signal<string | null>(this.spremljeno?.korisnickoIme ?? null);
  uloga = signal<string | null>(this.spremljeno?.uloga ?? null);

  prijavljen = computed(() => !!this.token());
  admin = computed(() => this.uloga() === 'Admin');
  trener = computed(() => this.uloga() === 'Trener');
  igrac = computed(() => this.uloga() === 'Igrac');

  prijava(korisnickoIme: string, lozinka: string): Observable<PrijavaOdgovor> {
    return this.http
      .post<PrijavaOdgovor>(`${BASE_URL}/auth/login`, { KorisnickoIme: korisnickoIme, Lozinka: lozinka })
      .pipe(
        tap((odgovor) => {
          this.token.set(odgovor.access_token);
          this.korisnickoIme.set(odgovor.KorisnickoIme);
          this.uloga.set(odgovor.Uloga);
          localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify({
              token: odgovor.access_token,
              korisnickoIme: odgovor.KorisnickoIme,
              uloga: odgovor.Uloga,
            }),
          );
        }),
      );
  }

  odjava(): void {
    this.token.set(null);
    this.korisnickoIme.set(null);
    this.uloga.set(null);
    localStorage.removeItem(STORAGE_KEY);
  }

  private procitajIzStorage(): SpremljenaPrijava | null {
    const sirovo = localStorage.getItem(STORAGE_KEY);
    if (!sirovo) return null;
    try {
      return JSON.parse(sirovo) as SpremljenaPrijava;
    } catch {
      return null;
    }
  }
}
