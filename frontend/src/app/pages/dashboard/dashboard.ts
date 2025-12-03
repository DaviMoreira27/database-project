import { Component, OnInit, signal } from '@angular/core';
import { ChartModule } from 'primeng/chart';
import { Header } from '../../components/header/header';
import { NavbarComponent } from '../../components/navbar/navbar';
import { inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastService } from '../../services/toast-service';
import { LoggedUser } from '../login/login';
import { Router } from '@angular/router';
import { forkJoin } from 'rxjs';
import { environment } from '../../../environments/environment.development';
import { ChartData } from 'chart.js';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

// Tipagens -------------------------

export interface TotensAtivos {
  n_registro: string;
}

export interface ReceitaMensal {
  mes: string;
  receita: number;
}

export interface TaxaOcupacao {
  n_registro: string;
  capacidade: number;
  bicicletas_disponiveis: number;
  taxa_ocupacao: number;
}

export interface ProblemasPorAvaliacao {
  n_registro: string;
  problemas: number;
  avaliacoes: number;
  razao_problema_por_avaliacao: number;
}

export interface BicicletasEstacionadas {
  ponto_retirada: string;
  total_estacionadas: number;
  estacionadas_no_ponto: number;
  percentual_relacional: number;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  imports: [NavbarComponent, Header, ChartModule, ProgressSpinnerModule],
})
export class Dashboard implements OnInit {
  private readonly httpService = inject(HttpClient);
  private readonly toastService = inject(ToastService);
  private readonly router = inject(Router);

  protected loading = signal(true);

  // Dados para os gráficos -----------------------------

  protected estacionamentoData!: ChartData<'bar'>;
  protected problemasData!: ChartData<'bar'>;
  protected bicicletasData!: ChartData<'bar'>;
  protected receitaData!: ChartData<'line'>;

  protected totensAtivosData!: ChartData<'bar'>;    
  protected totensAtivosDataBrute: TotensAtivos[] = []; 

  // Dados brutos --------------------------------------

  protected bicicletasEstacionadasDataBrute: BicicletasEstacionadas[] = [];
  protected problemasPorAvaliacaoDataBrute: ProblemasPorAvaliacao[] = [];
  protected taxaOcupacaoDataBrute: TaxaOcupacao[] = [];
  protected receitaMensalDataBrute: ReceitaMensal[] = [];

  // Opções visuais -------------------------------------

  protected readonly compactOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          boxWidth: 12,
          font: { size: 10 },
        },
      },
    },
    scales: {
      x: { display: true, grid: { display: true } },
      y: { display: true, grid: { display: true }, beginAtZero: true },
    },
  };

  ngOnInit(): void {
    const userData = JSON.parse(localStorage.getItem('user') ?? '') as LoggedUser['user'];

    if (!userData.provedora) {
      this.toastService.error('Nao foi possivel obter as informacoes do usuario');
      this.router.navigate(['/login'], { replaceUrl: true });
      return;
    }

    const cnpj = userData.provedora;

    // Requisições ------------------------------------------

    const totensAtivos$ = this.httpService.get<TotensAtivos[]>(
      `${environment.baseUrl}/totens-ativos/${cnpj}`,
    );

    const receitaMensal$ = this.httpService.get<ReceitaMensal[]>(
      `${environment.baseUrl}/receita-mensal/${cnpj}`,
    );

    const taxaOcupacao$ = this.httpService.get<TaxaOcupacao[]>(
      `${environment.baseUrl}/taxa-ocupacao/${cnpj}`,
    );

    const problemasPorAvaliacao$ = this.httpService.get<ProblemasPorAvaliacao[]>(
      `${environment.baseUrl}/problemas-por-avaliacao/${cnpj}`,
    );

    const bicicletasEstacionadas$ = this.httpService.get<BicicletasEstacionadas[]>(
      `${environment.baseUrl}/bicicletas-estacionadas/${cnpj}`,
    );

    // Execução em paralelo ---------------------------------

    forkJoin({
      totensAtivos: totensAtivos$,
      receitaMensal: receitaMensal$,
      taxaOcupacao: taxaOcupacao$,
      problemasPorAvaliacao: problemasPorAvaliacao$,
      bicicletasEstacionadas: bicicletasEstacionadas$,
    }).subscribe({
      next: (data) => {
        // Totens ativos todos os dias --------------------------------
        this.totensAtivosDataBrute = data.totensAtivos;

        this.totensAtivosData = {
          labels: this.totensAtivosDataBrute.map((d) => d.n_registro),
          datasets: [
            {
              label: 'Totens ativos todos os dias',
              data: this.totensAtivosDataBrute.map(() => 1),
              backgroundColor: '#42A5F5',
            },
          ],
        };

        // Receita Mensal ----------------------------------------------
        this.receitaMensalDataBrute = data.receitaMensal.map((d) => ({
          ...d,
          receita: Number(d.receita),
        }));

        const labelsReceita = this.receitaMensalDataBrute.map((d) => {
          const date = new Date(d.mes);
          return new Intl.DateTimeFormat('pt-BR', {
            month: 'long',
            year: 'numeric',
          }).format(date);
        });

        this.receitaData = {
          labels: labelsReceita,
          datasets: [
            {
              label: 'Receita',
              data: this.receitaMensalDataBrute.map((d) => d.receita),
              fill: false,
              borderColor: '#42A5F5',
              tension: 0.1,
            },
          ],
        };

        // Ocupação -----------------------------------------------
        this.taxaOcupacaoDataBrute = data.taxaOcupacao.map((d) => ({
          ...d,
          capacidade: Number(d.capacidade),
          bicicletas_disponiveis: Number(d.bicicletas_disponiveis),
          taxa_ocupacao: Number(d.taxa_ocupacao),
        }));

        this.bicicletasData = {
          labels: this.taxaOcupacaoDataBrute.map((d) => d.n_registro),
          datasets: [
            {
              label: 'Capacidade',
              data: this.taxaOcupacaoDataBrute.map((d) => d.capacidade),
              backgroundColor: '#FFA726',
            },
            {
              label: 'Bicicletas disponíveis',
              data: this.taxaOcupacaoDataBrute.map((d) => d.bicicletas_disponiveis),
              backgroundColor: '#66BB6A',
            },
          ],
        };

        // Problemas por avaliação --------------------------------------
        this.problemasPorAvaliacaoDataBrute = data.problemasPorAvaliacao;

        this.problemasData = {
          labels: this.problemasPorAvaliacaoDataBrute.map((d) => d.n_registro),
          datasets: [
            {
              label: 'Problemas',
              data: this.problemasPorAvaliacaoDataBrute.map((d) => d.problemas),
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#8E44AD'],
            },
          ],
        };

        // Frota estacionada -------------------------------------------
        this.bicicletasEstacionadasDataBrute = data.bicicletasEstacionadas;

        this.estacionamentoData = {
          labels: this.bicicletasEstacionadasDataBrute.map((d) => d.ponto_retirada),
          datasets: [
            {
              label: 'Estacionadas no ponto',
              data: this.bicicletasEstacionadasDataBrute.map((d) => d.estacionadas_no_ponto),
              backgroundColor: '#42A5F5',
            },
            {
              label: 'Total estacionadas',
              data: this.bicicletasEstacionadasDataBrute.map((d) => d.total_estacionadas),
              backgroundColor: '#9CCC65',
            },
          ],
        };

        this.loading.set(false);
      },
      error: (err) => {
        this.toastService.error('Falha ao carregar dados do dashboard');
        console.error(err);
        this.loading.set(false);
      },
    });
  }
}
