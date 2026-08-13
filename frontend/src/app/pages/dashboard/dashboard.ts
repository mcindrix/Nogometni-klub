import { Component, OnInit, inject, signal } from '@angular/core';
import { CurrencyPipe } from '@angular/common';

import { Api } from '../../services/api';
import { DashboardStatistika } from '../../models/models';

@Component({
  selector: 'app-dashboard',
  imports: [CurrencyPipe],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  private api = inject(Api);

  statistika = signal<DashboardStatistika | null>(null);
  greska = signal<string | null>(null);

  ngOnInit(): void {
    this.api.getDashboard().subscribe({
      next: (podaci) => this.statistika.set(podaci),
      error: () => this.greska.set('Ne mogu dohvatiti statistiku. Je li backend pokrenut na :8000?'),
    });
  }
}
