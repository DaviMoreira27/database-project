import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { SelectModule } from 'primeng/select';
import { ButtonModule } from 'primeng/button';
import { timer } from 'rxjs';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { ToastService } from '../../services/toast-service';
import { Router } from '@angular/router';

export interface LoggedUser {
  message: string;
  user: {
    cpf: string;
    cargo: string;
    nome: string;
    email: string;
    data_nascimento: string;
    provedora?: string;
  };
  error?: string;
}

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, InputTextModule, PasswordModule, SelectModule, ButtonModule],
  templateUrl: './login.html',
})
export class Login {
  private readonly httpService = inject(HttpClient);
  private readonly toastService = inject(ToastService);
  private readonly router = inject(Router);

  protected readonly roles = [
    { label: 'Gerente', value: 'GERENTE' },
  ];

  protected loading = signal(false);

  form = new FormGroup({
    email: new FormControl('', { validators: [Validators.required], nonNullable: true }),
    password: new FormControl('', { validators: [Validators.required], nonNullable: true }),
    role: new FormControl('', { validators: [Validators.required], nonNullable: true }),
  });

  submit() {
    if (!this.form.valid) {
      console.log('Invalid form');
      return;
    }

    this.loading.set(true);
    this.httpService
      .post<LoggedUser>(`${environment.baseUrl}/login`, {
        email: this.form.get('email')?.value,
        password: this.form.get('password')?.value,
        login_type: this.form.get('role')?.value,
      })
      .subscribe({
        next: (response) => {
          this.router.navigate(['/dashboard']);
          localStorage.setItem('user', JSON.stringify(response.user));
          this.toastService.success(response.message ?? 'Usuário logado com sucesso');
        },
        error: (err) => {
          this.toastService.error('Falha ao realizar login');
          console.error(err);
          this.loading.set(false);
        },
        complete: () => {
          this.loading.set(false);
        },
      });
    timer(5000).subscribe(() => {
      console.log(this.form.getRawValue());
      this.loading.set(false);
    });
  }
}
