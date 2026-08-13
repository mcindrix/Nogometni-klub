import { inject } from '@angular/core';
import { CanActivateChildFn, Router } from '@angular/router';

import { Auth } from './auth';

export const authGuard: CanActivateChildFn = (childRoute) => {
  const auth = inject(Auth);
  const router = inject(Router);

  if (!auth.prijavljen()) {
    return router.createUrlTree(['/login']);
  }
  const dozvoljeneUloge: string[] | undefined = childRoute.data['dozvoljeneUloge'];
  if (dozvoljeneUloge && !dozvoljeneUloge.includes(auth.uloga() ?? '')) {
    return router.createUrlTree(['/dashboard']);
  }
  return true;
};
