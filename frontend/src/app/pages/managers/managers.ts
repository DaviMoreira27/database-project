import { Component, signal, computed } from '@angular/core';
import { NavbarComponent } from '../../components/navbar/navbar';
import { Header } from '../../components/header/header';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { SelectModule } from 'primeng/select';

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
  ],
  templateUrl: './managers.html',
})
export class Managers {
  search = signal('');
  modalOpen = signal(false);

  roles = [{ label: 'Gerente', value: 'Gerente' }];

  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      cpf: ['', Validators.required],
      nome: ['', Validators.required],
      email: ['', Validators.required],
      cargo: ['Gerente'],
      cep: ['', Validators.required],
      rua: ['', Validators.required],
      numero: ['', Validators.required],
      data_nascimento: [''],
      senha: [''],
    });
  }

  data = signal<Manager[]>([
    {
      cpf: '123.456.789-00',
      nome: 'João da Silva',
      email: 'joao@empresa.com',
      cargo: 'Supervisor',
    },
    {
      cpf: '987.654.321-00',
      nome: 'Maria Souza',
      email: 'maria@empresa.com',
      cargo: 'Coordenadora',
    },
    { cpf: '111.222.333-44', nome: 'Pedro Almeida', email: 'pedro@empresa.com', cargo: 'Gerente' },
  ]);

  filtereds = computed(() => {
    const term = this.search().toLowerCase();
    return this.data().filter(
      (item) =>
        item.cpf.toLowerCase().includes(term) ||
        item.nome.toLowerCase().includes(term) ||
        item.email.toLowerCase().includes(term) ||
        item.cargo.toLowerCase().includes(term),
    );
  });

  newManager() {
    this.form.reset({ cargo: 'Gerente' });
    this.modalOpen.set(true);
  }

  save() {
    if (this.form.invalid) return;

    console.log('Salvar:', this.form.value);

    this.modalOpen.set(false);
  }

  updateSearch(value: any) {
    this.search.set(value.target.value);
  }

  onHideModal() {
    console.log('Trying');
  }
}
