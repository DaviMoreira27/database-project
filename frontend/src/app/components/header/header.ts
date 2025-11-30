import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ToastService } from '../../services/toast-service';
import { LoggedUser } from '../../pages/login/login';

@Component({
  selector: 'app-header',
  templateUrl: './header.html',
})
export class Header implements OnInit {
  private readonly toastService = inject(ToastService);
  private readonly router = inject(Router);

  protected userName?: string;

  ngOnInit(): void {
    const userData = JSON.parse(localStorage.getItem('user') ?? '') as LoggedUser['user'];

    if (userData.nome) {
      this.userName = userData.nome;
    }
  }

  logout() {
    localStorage.removeItem('user');
    this.toastService.success('Usuario deslogado com sucesso');
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}
