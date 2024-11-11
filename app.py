from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)

# Variável para armazenar o status
status_messages = []

def detect_phone_column(df):
    """Detecta automaticamente a coluna que contém números de telefone."""
    for column in df.columns:
        if df[column].astype(str).str.match(r'^\d{10,13}$').any():
            return column
    return None

def send_messages_via_whatsapp(numbers, message):
    """Envia mensagens para uma lista de números de telefone no WhatsApp Web usando Selenium."""
    global status_messages
    status_messages.clear()  # Limpa a lista de status para nova sessão

    # Inicializa o WebDriver
    service = Service("./chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # Abre o WhatsApp Web e espera que você escaneie o QR Code
    driver.get("https://web.whatsapp.com")
    status_messages.append("Conectando ao WhatsApp Web. Escaneie o QR Code.")
    time.sleep(20)  # Tempo para escanear o QR Code (ajuste conforme necessário)
    status_messages.append("Conexão estabelecida com sucesso.")

    # Para cada número, abre a conversa e envia a mensagem automaticamente
    for number in numbers:
        # Vai diretamente para a URL de envio de mensagem para o número
        driver.get(f"https://web.whatsapp.com/send?phone={number}&text={message}")
        try:
            # Espera o botão de envio aparecer e clica para enviar a mensagem
            send_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
            )
            send_button.click()
            status_messages.append(f"Mensagem enviada para {number}")

        except Exception as e:
            status_messages.append(f"Erro ao enviar para {number}: {e}")
        
        time.sleep(3)  # Pausa para evitar bloqueio e garantir tempo de processamento

    # Fecha o navegador após enviar todas as mensagens
    driver.quit()
    status_messages.append("Envio de mensagens concluído.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirm', methods=['POST'])
def confirm():
    message = request.form['message']
    file = request.files['file']
    file_path = os.path.join("uploads", file.filename)
    
    # Salvar o arquivo temporariamente
    file.save(file_path)

    # Verificar o tipo de arquivo e ler o conteúdo com o método adequado
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
    elif file.filename.endswith('.xls'):
        df = pd.read_excel(file_path, engine='xlrd')
    elif file.filename.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        os.remove(file_path)
        return "Formato de arquivo não suportado. Envie um arquivo .csv, .xls ou .xlsx."

    # Detectar a coluna que contém números de telefone
    phone_column = detect_phone_column(df)
    if not phone_column:
        os.remove(file_path)
        return "Não foi possível encontrar uma coluna de números de telefone no arquivo."

    # Extrair números de telefone
    numbers = df[phone_column].dropna().astype(str).tolist()
    os.remove(file_path)

    # Renderiza a página de confirmação com a lista de números e a mensagem
    return render_template('confirm.html', message=message, numbers=numbers)

@app.route('/send_messages', methods=['POST'])
def send_messages():
    message = request.form['message']
    numbers = request.form.getlist('numbers')
    try:
        send_messages_via_whatsapp(numbers, message)
        return redirect(url_for('status'))
    except Exception as e:
        return f"Erro ao enviar mensagens: {e}"

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/get_status')
def get_status():
    return jsonify(status_messages)

if __name__ == '__main__':
    app.run(debug=True)
