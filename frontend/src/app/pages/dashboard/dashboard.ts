import { Component } from '@angular/core';
import { ChartModule } from 'primeng/chart';
import { Header } from '../../components/header/header';
import { NavbarComponent } from '../../components/navbar/navbar';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  imports: [NavbarComponent, Header, ChartModule],
})
export class Dashboard {
  compactOptions = {
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
      x: {
        display: true, // Remove labels e linha do eixo X
        grid: {
          display: true, // Remove a grade vertical
        },
      },
      y: {
        display: true, // Remove os números (0.5, 1.0) do eixo Y
        grid: {
          display: true, // Remove a grade horizontal (os "círculos" ou linhas)
        },
        beginAtZero: true, // Garante que o gráfico comece do 0 mesmo sem mostrar
      },
    },
    elements: {
      point: {
        radius: 0, // Remove o ponto padrão
        hitRadius: 10, // Mantém a área clicável/hover
        hoverRadius: 4, // Mostra o ponto só quando passa o mouse
      },
    },
  };

  // Estacionamento por ponto
  estacionamentoJson = [
    {
      ponto_retirada: 'P10',
      total_estacionadas: 3,
      estacionadas_no_ponto: 2,
      percentual_relacional: 0.6667,
    },
    {
      ponto_retirada: 'P20',
      total_estacionadas: 3,
      estacionadas_no_ponto: 1,
      percentual_relacional: 0.3333,
    },
    {
      ponto_retirada: 'P30',
      total_estacionadas: 3,
      estacionadas_no_ponto: 0,
      percentual_relacional: 0.0,
    },
  ];

  estacionamentoData = {
    labels: this.estacionamentoJson.map((d) => d.ponto_retirada),
    datasets: [
      {
        label: 'Estacionadas no ponto',
        data: this.estacionamentoJson.map((d) => d.estacionadas_no_ponto),
        backgroundColor: '#42A5F5',
      },
      {
        label: 'Total estacionadas',
        data: this.estacionamentoJson.map((d) => d.total_estacionadas),
        backgroundColor: '#9CCC65',
      },
    ],
  };

  // Problemas por registro
  problemasJson = [
    { n_registro: 'INF1', problemas: 2, avaliacoes: 2, razao_problema_por_avaliacao: 1.0 },
    { n_registro: 'INF2', problemas: 0, avaliacoes: 1, razao_problema_por_avaliacao: 0.0 },
    { n_registro: 'INF3', problemas: 1, avaliacoes: 0, razao_problema_por_avaliacao: null },
  ];

  problemasData = {
    labels: this.problemasJson.map((d) => d.n_registro),
    datasets: [
      {
        label: 'Problemas',
        data: this.problemasJson.map((d) => d.problemas),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      },
    ],
  };

  // Bicicletas por ponto
  bicicletasJson = [
    { n_registro: 'P1', capacidade: 10, bicicletas_disponiveis: 4 },
    { n_registro: 'P2', capacidade: 6, bicicletas_disponiveis: 6 },
  ];

  bicicletasData = {
    labels: this.bicicletasJson.map((d) => d.n_registro),
    datasets: [
      {
        label: 'Capacidade',
        data: this.bicicletasJson.map((d) => d.capacidade),
        backgroundColor: '#FFA726',
      },
      {
        label: 'Bicicletas disponíveis',
        data: this.bicicletasJson.map((d) => d.bicicletas_disponiveis),
        backgroundColor: '#66BB6A',
      },
    ],
  };

  // Receita por mês
  receitaJson = [
    { mes: '2025-01-01', receita: 3000.0 },
    { mes: '2025-02-01', receita: 6423.0 },
  ];

  private mesesFormatadosReceita = this.receitaJson.map((d) => {
    const data = new Date(d.mes);
    const mesAno = new Intl.DateTimeFormat('pt-BR', { month: 'long', year: 'numeric' }).format(
      data,
    );
    return mesAno.charAt(0).toUpperCase() + mesAno.slice(1);
  });

  receitaData = {
    labels: this.mesesFormatadosReceita,
    datasets: [
      {
        label: 'Receita',
        data: this.receitaJson.map((d) => d.receita),
        fill: false,
        borderColor: '#42A5F5',
        tension: 0.1,
      },
    ],
  };

  // Sessões por dia
  sessoesJson = [
    { data: '2025-01-05', total_sessoes: 2 },
    { data: '2025-01-06', total_sessoes: 3 },
  ];

  private mesesFormatadosSessoes = this.sessoesJson.map((d) => {
    const [ano, mes, dia] = d.data.split('-');
    const meses = [
      'Janeiro',
      'Fevereiro',
      'Março',
      'Abril',
      'Maio',
      'Junho',
      'Julho',
      'Agosto',
      'Setembro',
      'Outubro',
      'Novembro',
      'Dezembro',
    ];
    return `${dia} ${meses[parseInt(mes, 10) - 1]}`;
  });

  sessoesData = {
    labels: this.mesesFormatadosSessoes,
    datasets: [
      {
        label: 'Total de sessões',
        data: this.sessoesJson.map((d) => d.total_sessoes),
        fill: false,
        borderColor: '#FF6384',
        tension: 0.1,
      },
    ],
  };
}
