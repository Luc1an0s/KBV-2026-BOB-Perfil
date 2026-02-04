# Alerta de Preenchimento - Controle de Produção
Este projeto automatiza a verificação de preenchimento de planilhas do Google Sheets. Caso a planilha não seja atualizada por 2 dias ou mais (ignorando domingos), o script envia um alerta automático via WhatsApp para os gestores responsáveis.

🚀 Funcionalidades
Leitura Automática: Integração com Google Sheets API.

Lógica de Data: Identifica o último registro e calcula o atraso.

Filtro de Calendário: Ignora domingos na contagem de dias de atraso.

Notificação: Disparo de mensagens via API de WhatsApp (Bubble).

Execução Agendada: Roda automaticamente todos os dias às 18:00 (Horário de Manaus) via GitHub Actions.

🛠️ Tecnologias Utilizadas
Python 3.12

Gspread: Manipulação da API do Google Sheets.

Requests: Comunicação com a API de mensagens.

Pytz: Gestão de fuso horário (America/Manaus).

GitHub Actions: Automação e agendamento (Cron).
