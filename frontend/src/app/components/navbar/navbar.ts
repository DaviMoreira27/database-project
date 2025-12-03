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
  ];

  toggleSidebar() {
    this.visible.update((v) => !v);
  }
}
