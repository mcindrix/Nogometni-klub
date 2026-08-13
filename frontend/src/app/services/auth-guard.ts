import { inject } from '@angular/core';
import { CanActivateChildFn, Router } from '@angular/router';

import { Auth } from './auth';

export const authGuard: CanActivateChildFn = (childRoute) => {
  const auth = inject(Auth);
  const router = inject(Router);

  if (!auth.prijavljen()) {
    return router.createUrlTree(['/login']);
  }
  if (childRoute.data['samoAdmin'] && !auth.admin()) {
    return router.createUrlTree(['/dashboard']);
  }
  return true;
};
