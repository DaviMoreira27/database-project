import { Component, signal, WritableSignal } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { MessageModule } from 'primeng/message';

@Component({
  selector: 'app-root',
  imports: [ButtonModule, MessageModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected signalInt: WritableSignal<number> = signal(0);

  protected readonly title = signal('Clean-City');

  protected clickUpdateUi() {
    this.signalInt.set(this.signalInt() + 1);
  }
}
