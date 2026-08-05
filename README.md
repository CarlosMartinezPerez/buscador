# 🎓 Buscador Automático de Editais & Bolsas em TI

Aplicativo em Python com Inteligência Artificial (Google Gemini API) que busca diariamente por editais de **capacitação tecnológica, residências de software e bolsas de estudo** (Web, IA, Machine Learning, IoT, Sistemas Embarcados) e envia um e-mail matinal formatado com as oportunidades inéditas.

---

## 🛠️ Como Funciona
1. **Busca Inteligente**: Pesquisa por editais em portais de fomento e redes de inovação (MCTI, Softex, EMBRAPII, FAPs, Institutos de Pesquisa).
2. **Filtragem com IA (Gemini)**: Analisa o conteúdo das páginas encontradas e avalia se o edital realmente é da área de TI, oferece bolsa de estudo/remuneração e se está aberto.
3. **Deduplicação (SQLite)**: Garante que você **nunca receba o mesmo edital mais de uma vez**.
4. **Envio de E-mail**: Envia um e-mail HTML limpo e responsivo com os novos editais.
5. **Automação Gratuita**: Roda automaticamente todas as manhãs no **GitHub Actions** sem gastar nada.

---

## 🚀 Testando Localmente

### 1. Clonar e preparar o ambiente
```bash
cd /home/carlos/buscador
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar o arquivo `.env`
Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```
Preencha suas chaves no `.env`:
* `GEMINI_API_KEY`: Obtenha gratuitamente no [Google AI Studio](https://aistudio.google.com/).
* `SMTP_USER` e `SMTP_PASSWORD`: Seu e-mail e Senha de App (ex: Gmail).
* `NOTIFY_EMAIL`: O e-mail onde você quer receber o resumo matinal.

---

## 🧪 Comandos de Teste

### Testar apenas a busca web (sem usar API de e-mail ou IA):
```bash
python main.py --test-search
```

### Simular o processo completo sem enviar e-mail real nem alterar o banco (Dry-Run):
```bash
python main.py --dry-run
```

### Enviar um e-mail de teste para verificar suas credenciais SMTP:
```bash
python main.py --test-email
```

---

## ☁️ Como Rodar no GitHub Actions (100% Grátis)

1. Crie um repositório no GitHub (pode ser público ou privado).
2. Envie este código para o seu repositório.
3. No GitHub, acesse **Settings > Secrets and variables > Actions**.
4. Adicione os seguintes **New repository secrets**:
   * `GEMINI_API_KEY`
   * `SMTP_SERVER` (ex: `smtp.gmail.com`)
   * `SMTP_PORT` (ex: `587`)
   * `SMTP_USER`
   * `SMTP_PASSWORD`
   * `NOTIFY_EMAIL`
5. Pronto! O GitHub Actions irá rodar o script automaticamente **todos os dias às 08:11 da manhã, aproximadamente, dependendo da carga do provedor** (horário de Brasília).
