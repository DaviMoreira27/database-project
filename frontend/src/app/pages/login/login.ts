import { Component, signal } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { SelectModule } from 'primeng/select';
import { ButtonModule } from 'primeng/button';
import { timer } from 'rxjs';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, InputTextModule, PasswordModule, SelectModule, ButtonModule],
  templateUrl: './login.html',
})
export class Login {
  protected readonly roles = [
    { label: 'Customer', value: 'customer' },
    { label: 'Manager', value: 'manager' },
    { label: 'Administrator', value: 'admin' },
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
    timer(5000).subscribe(() => {
      console.log(this.form.getRawValue());
      this.loading.set(false);
    });
  }
}
