import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { Auth } from './services/auth';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  auth = inject(Auth);
  private router = inject(Router);

  odjava(): void {
    this.auth.odjava();
    this.router.navigateByUrl('/login');
  }
}
