
# Automação de Envio de Mensagens pelo WhatsApp Web

Este projeto é uma aplicação web desenvolvida em Python com Flask e Selenium para automatizar o envio de mensagens em massa via WhatsApp Web. Com ele, você pode fazer o upload de uma lista de números de telefone, escrever uma mensagem personalizada e enviar a mensagem para todos os números da lista automaticamente, sem precisar adicionar os contatos manualmente.

## Funcionalidades

- **Carregar Lista de Números**: Faça o upload de um arquivo com números de telefone nos formatos `.csv`, `.xls` ou `.xlsx`. O sistema detecta automaticamente a coluna que contém os números de telefone.
- **Mensagem Personalizada**: Insira uma mensagem que será enviada para cada número da lista.
- **Automação do Envio pelo WhatsApp Web**: O sistema abre o WhatsApp Web, onde você escaneia o código QR uma única vez. A partir daí, o sistema envia automaticamente a mensagem para cada número da lista.
- **Status de Envio**: Acompanhe o status de envio para cada número e veja possíveis erros diretamente na interface do aplicativo.

## Pré-requisitos

- **Python 3.x** instalado
- **Google Chrome** instalado
- **ChromeDriver** compatível com a versão do Google Chrome

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie um ambiente virtual:

   ```bash
   python -m venv env
   ```

3. Ative o ambiente virtual:

   - No Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - No Mac/Linux:
     ```bash
     source env/bin/activate
     ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Certifique-se de que o **ChromeDriver** está na pasta do projeto ou no PATH do sistema. [Baixe o ChromeDriver aqui](https://chromedriver.chromium.org/downloads) se necessário.

## Uso

1. **Execute a aplicação**:

   ```bash
   python app.py
   ```

2. **Acesse o aplicativo** no seu navegador:

   Abra o navegador e vá para [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. **Carregue a lista de números**:

   - Faça o upload de um arquivo `.csv`, `.xls` ou `.xlsx` com os números de telefone.
   - Insira a mensagem que deseja enviar para todos os números.

4. **Confirme o envio**:

   - Após revisar a lista de números e a mensagem, clique em "Enviar".
   - O WhatsApp Web será aberto, onde você deve escanear o código QR para iniciar a sessão.

5. **Acompanhe o Status**:

   - O sistema exibirá o status de envio para cada número.

## Estrutura do Projeto

```plaintext
.
├── app.py                   # Arquivo principal da aplicação Flask
├── templates/
│   ├── index.html           # Página principal para upload e entrada de mensagem
│   └── confirm.html         # Página de confirmação de envio
├── static/
│   └── css/
│       └── styles.css       # Estilos da página
├── requirements.txt         # Lista de dependências do Python
└── chromedriver.exe         # ChromeDriver (coloque a versão compatível com o seu Chrome)
```

## Observações

- Este projeto utiliza o Selenium para controlar o navegador. Certifique-se de que o Google Chrome e o ChromeDriver estão atualizados.
- Lembre-se de que o WhatsApp possui políticas contra spam e uso abusivo. Use esta ferramenta de forma responsável.

## Licença

Este projeto é licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para obter mais informações.
