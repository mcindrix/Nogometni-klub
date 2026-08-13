import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { Auth } from '../../services/auth';

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  private auth = inject(Auth);
  private router = inject(Router);

  korisnickoIme = '';
  lozinka = '';
  greska = signal<string | null>(null);

  prijava(): void {
    this.greska.set(null);
    this.auth.prijava(this.korisnickoIme, this.lozinka).subscribe({
      next: () => this.router.navigateByUrl('/dashboard'),
      error: (err) => this.greska.set(err.error?.detail ?? 'Prijava nije uspjela'),
    });
  }
}
