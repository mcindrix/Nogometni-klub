// TypeScript sucelja koja odgovaraju Pydantic shemama iz backend/schemas.py

export interface Pozicija {
  PozicijaID: number;
  Naziv: string;
  Opis: string | null;
}

export interface Stadion {
  StadionID: number;
  Naziv: string;
  Grad: string;
  Kapacitet: number | null;
}

export interface Trener {
  TrenerID: number;
  Ime: string;
  Prezime: string;
  Licenca: string | null;
  DatumRodjenja: string | null;
}

export interface Ekipa {
  EkipaID: number;
  Naziv: string;
  Liga: string | null;
}

export interface Igrac {
  IgracID: number;
  Ime: string;
  Prezime: string;
  DatumRodjenja: string | null;
  PozicijaID: number;
  EkipaID: number | null;
  pozicija: Pozicija;
  ekipa: Ekipa | null;
}

export interface Clanarina {
  ClanarinaID: number;
  IgracID: number;
  Iznos: number;
  DatumUplate: string;
  Razdoblje: string | null;
  igrac: Igrac;
}

export interface Utakmica {
  UtakmicaID: number;
  EkipaID: number;
  Protivnik: string;
  StadionID: number;
  DatumVrijeme: string;
  RezultatNas: number | null;
  RezultatProtivnik: number | null;
  ekipa: Ekipa;
  stadion: Stadion;
}

export interface Trening {
  TreningID: number;
  EkipaID: number;
  TrenerID: number;
  StadionID: number | null;
  DatumVrijeme: string;
  Trajanje: number | null;
  ekipa: Ekipa;
  trener: Trener;
  stadion: Stadion | null;
}

export interface PrijavaOdgovor {
  access_token: string;
  token_type: string;
  KorisnickoIme: string;
  Uloga: 'Admin' | 'Korisnik';
}

export interface DashboardStatistika {
  brojIgraca: number;
  brojEkipa: number;
  brojTrenera: number;
  brojUtakmica: number;
  brojTreninga: number;
  ukupnoClanarina: number;
}
