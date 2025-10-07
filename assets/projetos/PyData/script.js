// Aguarda o conteúdo da página ser totalmente carregado para iniciar o script
document.addEventListener('DOMContentLoaded', () => {

    // ===================================================================
    // VARIÁVEIS GLOBAIS
    // ===================================================================
    let dadosCompletos = []; // Armazenará todos os dados do JSON
    let charts = {}; // Objeto para manter as instâncias de todos os gráficos

    // ===================================================================
    // FUNÇÕES PRINCIPAIS
    // ===================================================================

    /**
     * Carrega os dados do arquivo JSON e inicia o dashboard.
     */
    async function carregarDados() {
        try {
            const response = await fetch('python/data/dashboard_data.json');
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.statusText}`);
            }
            dadosCompletos = await response.json();

            // Após carregar os dados, popular os filtros e renderizar o estado inicial
            popularFiltros();
            aplicarFiltros();

        } catch (error) {
            console.error('Falha ao carregar ou processar os dados do dashboard:', error);
            alert('Não foi possível carregar os dados. Verifique o console para mais informações.');
        }
    }

    /**
     * Popula os campos <select> dos filtros com valores únicos dos dados.
     */
    function popularFiltros() {
        // Extrai valores únicos usando Sets para evitar duplicatas
        const anos = [...new Set(dadosCompletos.map(d => d.ano))].sort();
        const regioes = [...new Set(dadosCompletos.map(d => d.regiao))].sort();
        const vendedores = [...new Set(dadosCompletos.map(d => d.nome_usuario))].sort();
        const produtos = [...new Set(dadosCompletos.map(d => d.nome_servico))].sort();

        // Popula cada select com as opções
        popularSelect('filtro-ano', anos);
        popularSelect('filtro-regiao', regioes);
        popularSelect('filtro-vendedor', vendedores);
        popularSelect('filtro-produto', produtos);
    }

    /**
     * Aplica os filtros selecionados e atualiza toda a visualização de dados.
     */
    function aplicarFiltros() {
        // Pega os valores atuais dos filtros
        const filtros = {
            ano: document.getElementById('filtro-ano').value,
            regiao: document.getElementById('filtro-regiao').value,
            vendedor: document.getElementById('filtro-vendedor').value,
            produto: document.getElementById('filtro-produto').value,
        };

        // Filtra os dados com base nos valores selecionados
        const dadosFiltrados = dadosCompletos.filter(item => {
            return (filtros.ano ? item.ano == filtros.ano : true) &&
                (filtros.regiao ? item.regiao === filtros.regiao : true) &&
                (filtros.vendedor ? item.nome_usuario === filtros.vendedor : true) &&
                (filtros.produto ? item.nome_servico === filtros.produto : true);
        });

        // Atualiza os componentes do dashboard com os dados filtrados
        atualizarKPIs(dadosFiltrados);
        atualizarGraficos(dadosFiltrados);
    }

    // ===================================================================
    // FUNÇÕES DE ATUALIZAÇÃO DO DASHBOARD
    // ===================================================================

    /**
     * Atualiza os cards de KPI (Faturamento, Vendas, Ticket Médio).
     */
    function atualizarKPIs(dados) {
        const faturamentoTotal = dados.reduce((acc, item) => acc + item.faturamento, 0);

        // Para contar vendas únicas, usamos um Set com um identificador de cada venda original
        // Esta é uma aproximação, já que não temos o id_venda no JSON final.
        // A combinação de campos cria uma chave única por evento de venda agregado.
        const vendasUnicas = new Set(dados.map(d => `${d.ano}-${d.mes}-${d.regiao}-${d.nome_usuario}-${d.nome_servico}`)).size;

        const ticketMedio = vendasUnicas > 0 ? faturamentoTotal / vendasUnicas : 0;

        document.getElementById('valor-faturamento').textContent = formatarMoeda(faturamentoTotal);
        document.getElementById('valor-vendas').textContent = vendasUnicas;
        document.getElementById('valor-ticket-medio').textContent = formatarMoeda(ticketMedio);
    }

    /**
     * Orquestra a atualização de todos os gráficos.
     */
    function atualizarGraficos(dados) {
        const granularidadeEvolucao = document.querySelector('input[name="evolucao-granularidade"]:checked').value;

        // Chama a função de atualização para cada gráfico
        atualizarGraficoEvolucao(dados, granularidadeEvolucao);
        atualizarGraficoPizza('grafico-regiao', 'Vendas por Região', dados, 'regiao');
        atualizarGraficoBarras('grafico-produto', 'Vendas por Produto', dados, 'nome_servico');
        atualizarGraficoBarras('grafico-vendedor', 'Top 5 Vendedores', dados, 'nome_usuario', 5, true);
    }

    // ===================================================================
    // FUNÇÕES GENÉRICAS PARA GRÁFICOS (REUTILIZÁVEIS)
    // ===================================================================

    /**
     * Atualiza ou cria um gráfico de barras.
     */
    function atualizarGraficoBarras(idCanvas, titulo, dados, chaveAgrupamento, topN = null, horizontal = false) {
        const dadosAgrupados = agruparDados(dados, chaveAgrupamento, 'faturamento');

        let itens = Object.entries(dadosAgrupados).sort(([, a], [, b]) => b - a);
        if (topN) {
            itens = itens.slice(0, topN);
        }

        const labels = itens.map(([label]) => label);
        const valores = itens.map(([, valor]) => valor);

        const config = {
            type: horizontal ? 'bar' : 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: titulo,
                    data: valores,
                    backgroundColor: horizontal ? 'rgba(40, 167, 69, 0.7)' : 'rgba(255, 193, 7, 0.7)',
                    borderColor: horizontal ? 'rgba(40, 167, 69, 1)' : 'rgba(255, 193, 7, 1)',
                    borderWidth: 1,
                    indexAxis: horizontal ? 'y' : 'x',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
            }
        };

        criarOuAtualizarGrafico(idCanvas, config);
    }

    /**
     * Atualiza ou cria o gráfico de evolução de faturamento.
     */
    function atualizarGraficoEvolucao(dados, granularidade) {
        let chaveAgrupamento;
        if (granularidade === 'ano') chaveAgrupamento = ['ano'];
        if (granularidade === 'trimestre') chaveAgrupamento = ['ano', 'trimestre'];
        if (granularidade === 'mes') chaveAgrupamento = ['ano', 'mes'];

        const dadosAgrupados = dados.reduce((acc, item) => {
            const chave = chaveAgrupamento.map(k => {
                // Se a granularidade for 'mes' E a chave atual for 'mes', formate o valor
                if (granularidade === 'mes' && k === 'mes') {
                    return String(item[k]).padStart(2, '0');
                }
                // Para todos os outros casos, retorne o valor normal
                return item[k];
            }).join(granularidade === 'trimestre' ? '-T' : '-');

            if (!acc[chave]) acc[chave] = 0;
            acc[chave] += item.faturamento;
            return acc;
        }, {});

        const labels = Object.keys(dadosAgrupados).sort();
        const valores = labels.map(label => dadosAgrupados[label]);

        const config = {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Faturamento',
                    data: valores,
                    backgroundColor: 'rgba(0, 123, 255, 0.7)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true } }
            }
        };

        criarOuAtualizarGrafico('grafico-evolucao', config);
    }

    /**
     * Atualiza ou cria um gráfico de pizza.
     */
    function atualizarGraficoPizza(idCanvas, titulo, dados, chaveAgrupamento) {
        const dadosAgrupados = agruparDados(dados, chaveAgrupamento, 'faturamento');
        const labels = Object.keys(dadosAgrupados);
        const valores = Object.values(dadosAgrupados);

        const config = {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: titulo,
                    data: valores,
                    backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8'],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        };

        criarOuAtualizarGrafico(idCanvas, config);
    }

    /**
     * Função genérica para criar um novo gráfico ou atualizar um existente.
     */
    function criarOuAtualizarGrafico(idCanvas, config) {
        const context = document.getElementById(idCanvas).getContext('2d');
        if (charts[idCanvas]) {
            // Se o gráfico já existe, atualiza seus dados e re-renderiza
            charts[idCanvas].data = config.data;
            charts[idCanvas].options = config.options;
            charts[idCanvas].update();
        } else {
            // Se não existe, cria um novo
            charts[idCanvas] = new Chart(context, config);
        }
    }

    // ===================================================================
    // FUNÇÕES AUXILIARES
    // ===================================================================

    /**
     * Popula um elemento <select> com opções.
     */
    function popularSelect(id, opcoes) {
        const select = document.getElementById(id);
        select.innerHTML = '<option value="">Todos</option>'; // Opção padrão
        opcoes.forEach(opcao => {
            select.add(new Option(opcao, opcao));
        });
    }

    /**
     * Formata um número como moeda BRL.
     */
    function formatarMoeda(valor) {
        return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    }

    /**
     * Agrupa um array de objetos por uma chave e soma outra.
     */
    function agruparDados(array, chave, chaveSoma) {
        return array.reduce((acc, obj) => {
            const key = obj[chave];
            if (!acc[key]) acc[key] = 0;
            acc[key] += obj[chaveSoma];
            return acc;
        }, {});
    }

    // ===================================================================
    // EVENT LISTENERS
    // ===================================================================

    // Adiciona listeners aos botões de filtro
    document.getElementById('botao-aplicar').addEventListener('click', aplicarFiltros);
    document.getElementById('botao-resetar').addEventListener('click', () => {
        document.getElementById('form-filtros').reset();
        aplicarFiltros();
    });

    // Adiciona listeners aos radios de granularidade do gráfico de evolução
    document.querySelectorAll('input[name="evolucao-granularidade"]').forEach(radio => {
        radio.addEventListener('change', aplicarFiltros);
    });

    // ===================================================================
    // INICIALIZAÇÃO
    // ===================================================================
    carregarDados();

});
