import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

import { Auth } from './auth';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(Auth);
  const router = inject(Router);
  const token = auth.token();

  const zahtjev = token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req;

  return next(zahtjev).pipe(
    catchError((greska: HttpErrorResponse) => {
      if (greska.status === 401) {
        auth.odjava();
        router.navigate(['/login']);
      }
      return throwError(() => greska);
    }),
  );
};
