import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import pytz
import os
from datetime import datetime, timedelta

URL_API = "https://appbobinaskbv.bubbleapps.io/version-test/api/1.1/wf/enviamensagem"

def calcular_dias_sem_domingo(inicio, fim):
    dias_atraso = 0
    temp_data = inicio + timedelta(days=1)
    while temp_data <= fim:
        if temp_data.weekday() != 6:
            dias_atraso += 1
        temp_data += timedelta(days=1)
    return dias_atraso

def verificar_atraso_planilha():

    sheet_id = os.environ.get("SHEET_ID")
    nome_aba = os.environ.get("NOME_ABA")
    cred_json = os.environ.get("GOOGLE_CRED_JSON")
    
    if not all([sheet_id, nome_aba, cred_json]):
        raise RuntimeError("Faltam variáveis de ambiente (Secrets) no GitHub.")

    with open("temp_creds.json", "w") as f:
        f.write(cred_json)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id).worksheet(nome_aba)
    dados = sheet.get_all_values()
    headers = dados[0]
    linhas = dados[1:]

    try:
        idx_data = headers.index("DATA")
    except ValueError:
        print("Erro: Coluna 'DATA' não encontrada.")
        return

    fuso_manaus = pytz.timezone("America/Manaus")
    hoje = datetime.now(fuso_manaus).replace(hour=0, minute=0, second=0, microsecond=0)

    datas_encontradas = []
    for linha in linhas:
        if len(linha) > idx_data and linha[idx_data].strip():
            try:
                data_dt = datetime.strptime(linha[idx_data].strip(), "%d/%m/%Y").replace(tzinfo=fuso_manaus)
                datas_encontradas.append(data_dt)
            except:
                continue

    if not datas_encontradas:
        print("Nenhuma data encontrada.")
        return

    ultima_data = max(datas_encontradas).replace(hour=0, minute=0, second=0, microsecond=0)
    diferenca_util = calcular_dias_sem_domingo(ultima_data, hoje)

    if diferenca_util >= 2:
        enviar_alerta(diferenca_util, ultima_data.strftime('%d/%m/%Y'), nome_aba)
    
    if os.path.exists("temp_creds.json"):
        os.remove("temp_creds.json")

def enviar_alerta(dias, data_formatada, nome_aba):
    mensagem = (
        f"⚠ *ALERTA DE ATENÇÃO*\n\n"
        f"A planilha de Controle de Produção de Perfil não é preenchida há {dias} dias úteis.\n"
        f"Último preenchimento: {data_formatada}\n"
        f"Status: Necessita de atenção urgente."
    )

    numeros = os.environ.get("NUMEROS_WHATSAPP", "").split(",")
    for numero in numeros:
        if numero.strip():
            payload = {"celular": numero.strip(), "mensagem": mensagem}
            response = requests.post(URL_API, data=payload)
            print(f"Enviado para {numero}: {response.status_code}")

if __name__ == "__main__":
    verificar_atraso_planilha()