import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { Observable } from 'rxjs';

import {
  Clanarina,
  DashboardStatistika,
  Ekipa,
  Igrac,
  Pozicija,
  Stadion,
  Trener,
  Trening,
  Utakmica,
} from '../models/models';

const BASE_URL = 'http://localhost:8000/api';

@Service()
export class Api {
  private http = inject(HttpClient);

  // Pozicija
  getPozicije(): Observable<Pozicija[]> {
    return this.http.get<Pozicija[]>(`${BASE_URL}/pozicija`);
  }
  dodajPoziciju(podaci: Partial<Pozicija>): Observable<Pozicija> {
    return this.http.post<Pozicija>(`${BASE_URL}/pozicija`, podaci);
  }
  obrisiPoziciju(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE_URL}/pozicija/${id}`);
  }

  // Stadion
  getStadione(): Observable<Stadion[]> {
    return this.http.get<Stadion[]>(`${BASE_URL}/stadion`);
  }
  dodajStadion(podaci: Partial<Stadion>): Observable<Stadion> {
    return this.http.post<Stadion>(`${BASE_URL}/stadion`, podaci);
  }
  obrisiStadion(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE_URL}/stadion/${id}`);
  }

  // Trener
  getTrenere(): Observable<Trener[]> {
    return this.http.get<Trener[]>(`${BASE_URL}/trener`);
  }
  dodajTrenera(podaci: Partial<Trener>): Observable<Trener> {
    return this.http.post<Trener>(`${BASE_URL}/trener`, podaci);
  }
  obrisiTrenera(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE_URL}/trener/${id}`);
  }

  // Ekipa
  getEkipe(): Observable<Ekipa[]> {
    return this.http.get<Ekipa[]>(`${BASE_URL}/ekipa`);
  }
  dodajEkipu(podaci: Partial<Ekipa>): Observable<Ekipa> {
    return this.http.post<Ekipa>(`${BASE_URL}/ekipa`, podaci);
  }
  obrisiEkipu(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE_URL}/ekipa/${id}`);
  }

  // Igrac
  getIgrace(): Observable<Igrac[]> {
    return this.http.get<Igrac[]>(`${BASE_URL}/igrac`);
  }
  dodajIgraca(podaci: Partial<Igrac>): Observable<Igrac> {
    return this.http.post<Igrac>(`${BASE_URL}/igrac`, podaci);
  }
  obrisiIgraca(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE_URL}/igrac/${id}`);
  }

  // Clanarina
  getClanarine(): Observable<Clanarina[]> {
    return this.http.get<Clanarina[]>(`${BASE_URL}/clanarina`);
  }
  dodajClanarinu(podaci: Partial<Clanarina>): Observable<Clanarina> {
    return this.http.post<Clanarina>(`${BASE_URL}/clanarina`, podaci);
  }
  obrisiClanarinu(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE_URL}/clanarina/${id}`);
  }

  // Utakmica
  getUtakmice(): Observable<Utakmica[]> {
    return this.http.get<Utakmica[]>(`${BASE_URL}/utakmica`);
  }
  dodajUtakmicu(podaci: Partial<Utakmica>): Observable<Utakmica> {
    return this.http.post<Utakmica>(`${BASE_URL}/utakmica`, podaci);
  }
  obrisiUtakmicu(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE_URL}/utakmica/${id}`);
  }

  // Trening
  getTreninge(): Observable<Trening[]> {
    return this.http.get<Trening[]>(`${BASE_URL}/trening`);
  }
  dodajTrening(podaci: Partial<Trening>): Observable<Trening> {
    return this.http.post<Trening>(`${BASE_URL}/trening`, podaci);
  }
  obrisiTrening(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE_URL}/trening/${id}`);
  }

  // Dashboard
  getDashboard(): Observable<DashboardStatistika> {
    return this.http.get<DashboardStatistika>(`${BASE_URL}/dashboard`);
  }
}
