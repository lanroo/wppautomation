from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote

app = Flask(__name__)

status_messages = []

def load_message_from_file():
    try:
        with open("mensagem.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Arquivo de mensagem não encontrado. Verifique o arquivo 'mensagem.txt'."

def detect_phone_column(df):
    for column in df.columns:
        if df[column].astype(str).str.match(r'^\d{10,13}$').any():
            return column
    return None

def send_messages_via_whatsapp(numbers):
    global status_messages
    status_messages.clear()

    # Carrega a mensagem do arquivo e codifica para preservar a formatação
    message = load_message_from_file()
    encoded_message = quote(message)

    # Inicializa o WebDriver
    service = Service("./chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # Abre o WhatsApp Web e espera que você escaneie o QR Code
    driver.get("https://web.whatsapp.com")
    status_messages.append("Conectando ao WhatsApp Web. Escaneie o QR Code.")
    time.sleep(20)
    status_messages.append("Conexão estabelecida com sucesso.")

    for number in numbers:
        driver.get(f"https://web.whatsapp.com/send?phone={number}&text={encoded_message}")
        try:
            send_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
            )
            send_button.click()
            status_messages.append(f"Mensagem enviada para {number}")
        except Exception as e:
            status_messages.append(f"Erro ao enviar para {number}: {e}")
        
        time.sleep(3)

    driver.quit()
    status_messages.append("Envio de mensagens concluído.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirm', methods=['POST'])
def confirm():
    file = request.files['file']
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
    elif file.filename.endswith('.xls'):
        df = pd.read_excel(file_path, engine='xlrd')
    elif file.filename.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        os.remove(file_path)
        return "Formato de arquivo não suportado."

    phone_column = detect_phone_column(df)
    if not phone_column:
        os.remove(file_path)
        return "Não foi possível encontrar uma coluna de números de telefone no arquivo."

    numbers = df[phone_column].dropna().astype(str).tolist()
    os.remove(file_path)

    # Carrega a mensagem do arquivo para exibição na página de confirmação
    message = load_message_from_file()

    return render_template('confirm.html', message=message, numbers=numbers)

@app.route('/send_messages', methods=['POST'])
def send_messages():
    numbers = request.form.getlist('numbers')
    try:
        send_messages_via_whatsapp(numbers)
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
