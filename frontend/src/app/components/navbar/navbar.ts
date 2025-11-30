import { Component, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { DrawerModule } from 'primeng/drawer';
import { ButtonModule } from 'primeng/button';

interface MenuItem {
  label: string;
  icon: string;
  route: string;
}

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [DrawerModule, ButtonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
})
export class NavbarComponent {
  visible = signal(true);

  menuItems: MenuItem[] = [
    { label: 'Dashboard', icon: 'pi pi-home', route: '/dashboard' },
    { label: 'Gerentes', icon: 'pi pi-users', route: '/managers' },
    { label: 'Reports', icon: 'pi pi-chart-line', route: '/reports' },
    { label: 'Infraestrutura', icon: 'pi pi-inbox', route: '/infra' },
    { label: 'Configuracoes', icon: 'pi pi-cog', route: '/settings' },
    { label: 'Suporte', icon: 'pi pi-question-circle', route: '/support' },
  ];

  toggleSidebar() {
    this.visible.update((v) => !v);
  }
}
