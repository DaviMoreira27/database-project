import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { SelectModule } from 'primeng/select';
import { ButtonModule } from 'primeng/button';
import { timer } from 'rxjs';
import { HttpClient } from '@angular/common/http';
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

  // Injeção dos serviços principais
  private readonly httpService = inject(HttpClient);
  private readonly toastService = inject(ToastService);
  private readonly router = inject(Router);

  // Opções disponíveis para seleção de cargo durante o login.
  protected readonly roles = [
    { label: 'Gerente', value: 'GERENTE' },
  ];

  // Controle visual de carregamento mostrado no botão de login.
  protected loading = signal(false);

  // Estrutura do formulário
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

    // Timer de debug: apenas imprime os valores do formulário após 5 segundos.
    timer(5000).subscribe(() => {
      console.log(this.form.getRawValue());
      this.loading.set(false);
    });
  }
}
