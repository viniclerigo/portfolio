document.addEventListener('DOMContentLoaded', () => {
    // Seleciona o corpo da tabela onde os dados serão inseridos
    const tableBody = document.querySelector("#leadsTable tbody");

    // Usa a API Fetch para buscar os dados do arquivo JSON
    fetch('leads_processados.json')
        .then(response => {
            // Verifica se a requisição foi bem-sucedida
            if (!response.ok) {
                throw new Error('Erro ao carregar o arquivo JSON: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Itera sobre cada lead nos dados
            data.forEach(lead => {
                // Cria uma nova linha na tabela
                const row = document.createElement('tr');

                // Formata a data de vencimento (ou exibe 'N/A' se não houver)
                const dueDate = lead.dueTime_timestamp ? new Date(lead.dueTime_timestamp).toLocaleDateString() : 'N/A';

                // Formata o valor para a moeda local
                const leadValue = lead.value_amount.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

                // Preenche a linha com as células de dados do lead
                row.innerHTML = `
                    <td>${lead.id}</td>
                    <td>${lead.name}</td>
                    <td>${lead.status}</td>
                    <td>${lead.confidence}%</td>
                    <td>${leadValue}</td>
                    <td>${dueDate}</td>
                `;

                // Adiciona a linha preenchida ao corpo da tabela
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            // Exibe um erro no console se algo der errado
            console.error('Houve um problema com a operação de fetch:', error);
            // Opcional: exibe uma mensagem de erro na página
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:red;">Falha ao carregar os dados.</td></tr>`;
        });
});
