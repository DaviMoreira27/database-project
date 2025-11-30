import { Component, signal, computed, inject, OnInit } from '@angular/core';
import { NavbarComponent } from '../../components/navbar/navbar';
import { Header } from '../../components/header/header';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { SelectModule } from 'primeng/select';
import { ToastService } from '../../services/toast-service';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment.development';
import { LoggedUser } from '../login/login';
import { Router } from '@angular/router';
import { ProgressSpinner } from 'primeng/progressspinner';

interface Manager {
  cpf: string;
  nome: string;
  email: string;
  cargo: string;
}

@Component({
  selector: 'app-managers',
  imports: [
    NavbarComponent,
    Header,
    CommonModule,
    TableModule,
    InputTextModule,
    ButtonModule,
    DialogModule,
    SelectModule,
    ReactiveFormsModule,
    ProgressSpinner,
  ],
  templateUrl: './managers.html',
})
export class Managers implements OnInit {
  private readonly toastService = inject(ToastService);
  private readonly httpService = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly fb = inject(FormBuilder);

  private cnpj!: string;

  protected search = signal('');
  protected modalOpen = signal(false);
  protected data = signal<Manager[]>([]);

  protected loadingList = signal(true);
  protected loadingSave = signal(false);

  protected readonly roles = [{ label: 'Gerente', value: 'Gerente' }];
  protected readonly form: FormGroup = this.fb.group({
    cpf: ['', Validators.required],
    nome: ['', Validators.required],
    email: ['', Validators.required],
    cargo: ['Gerente'],
    cep: ['', Validators.required],
    rua: ['', Validators.required],
    numero: ['', Validators.required],
    cidade: ['', Validators.required],
    uf: ['', Validators.required, Validators.maxLength(2)],
    data_nascimento: ['', Validators.required],
    senha: ['', Validators.required],
  });

  ngOnInit(): void {
    const userData = JSON.parse(localStorage.getItem('user') ?? '') as LoggedUser['user'];

    if (!userData?.provedora) {
      this.toastService.error('Nao foi possivel obter as informacoes do usuario');
      this.router.navigate(['/login'], { replaceUrl: true });
      return;
    }

    this.cnpj = userData.provedora;

    this.httpService
      .get<Manager[]>(`${environment.baseUrl}/listar/GERENTE`, {
        params: {
          cnpj: userData.provedora,
        },
      })
      .subscribe({
        next: (response) => {
          this.data.set(response);
          this.loadingList.set(false);
        },
        error: () => {
          this.toastService.error('Erro carregando lista de gerentes');
          this.loadingList.set(false);
          this.router.navigate(['/login'], { replaceUrl: true });
        },
      });
  }

  filtereds = computed(() => {
    const term = this.search().toLowerCase();
    return this.data().filter((item) =>
      [item.cpf, item.nome, item.email, item.cargo].some((v) => v.toLowerCase().includes(term)),
    );
  });

  updateSearch(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.search.set(value);
  }

  newManager() {
    this.form.reset({
      cargo: 'Gerente',
      cidade: '',
      uf: '',
    });
    this.modalOpen.set(true);
  }

  save() {
    this.form.markAllAsTouched();
    if (this.form.invalid) {
      this.toastService.error('Voce deve preencher os campos antes de enviar o formulario!');
      return;
    }

    this.loadingSave.set(true);
    const body = {
      cpf: this.form.value.cpf,
      cargo: 'GERENTE',
      cep: this.form.value.cep,
      rua: this.form.value.rua,
      cidade: this.form.value.cidade,
      uf: this.form.value.uf,
      numero: this.form.value.numero,
      nome: this.form.value.nome,
      email: this.form.value.email,
      senha: this.form.value.senha,
      data_nascimento: this.form.value.data_nascimento,
      provedora: this.cnpj,
    };

    this.httpService.post(`${environment.baseUrl}/criar`, body).subscribe({
      next: () => {
        this.toastService.success('Gerente criado com sucesso!');
        this.modalOpen.set(false);

        this.httpService
          .get<Manager[]>(`${environment.baseUrl}/listar/GERENTE`, {
            params: {
              cnpj: this.cnpj,
            },
          })
          .subscribe({
            next: (updatedList) => this.data.set(updatedList),
          });

        this.loadingSave.set(false);
      },
      error: () => {
        this.toastService.error('Erro ao criar gerente');
        this.loadingSave.set(false);
      },
    });
  }
}
