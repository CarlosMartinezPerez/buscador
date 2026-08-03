import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
from config import Config

EMAIL_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f6f8;
            color: #1e293b;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 680px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #ffffff;
            padding: 30px 24px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 22px;
            font-weight: 700;
        }
        .header p {
            margin: 6px 0 0 0;
            font-size: 14px;
            color: #94a3b8;
        }
        .content {
            padding: 24px;
        }
        .card {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #4f46e5;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 20px;
        }
        .card-title {
            font-size: 17px;
            font-weight: 600;
            color: #0f172a;
            margin: 0 0 10px 0;
        }
        .badge {
            display: inline-block;
            background-color: #e0e7ff;
            color: #3730a3;
            font-size: 12px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 9999px;
            margin-right: 6px;
            margin-bottom: 6px;
        }
        .stipend-badge {
            background-color: #dcfce7;
            color: #166534;
        }
        .deadline-badge {
            background-color: #fef3c7;
            color: #92400e;
        }
        .summary {
            font-size: 14px;
            color: #334155;
            line-height: 1.5;
            margin: 12px 0;
        }
        .btn {
            display: inline-block;
            background-color: #4f46e5;
            color: #ffffff !important;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 6px;
            margin-top: 6px;
        }
        .footer {
            text-align: center;
            padding: 20px;
            font-size: 12px;
            color: #64748b;
            border-top: 1px solid #e2e8f0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Novas Bolsas & Capacitações em TI</h1>
            <p>Resumo diário automatizado • {{ date_str }}</p>
        </div>
        <div class="content">
            <p>Olá! Encontramos <strong>{{ editais|length }}</strong> nova(s) oportunidade(s) de capacitação em tecnologia com bolsa de estudos:</p>
            
            {% for item in editais %}
            <div class="card">
                <div class="card-title">{{ item.title }}</div>
                <div>
                    <span class="badge stipend-badge">💰 {{ item.stipend_info }}</span>
                    {% if item.deadline and item.deadline != "Não especificado" %}
                    <span class="badge deadline-badge">📅 Inscrições: {{ item.deadline }}</span>
                    {% endif %}
                    {% for topic in item.topics %}
                    <span class="badge">🏷️ {{ topic }}</span>
                    {% endfor %}
                </div>
                <div class="summary">{{ item.summary }}</div>
                <a href="{{ item.url }}" target="_blank" class="btn">Ver Edital Completo ➔</a>
            </div>
            {% endfor %}
        </div>
        <div class="footer">
            Enviado automaticamente pelo Buscador de Editais de TI • Projeto Open Source
        </div>
    </div>
</body>
</html>
"""

def send_notification_email(editais: List[Dict], dry_run: bool = False) -> bool:
    """Sends HTML email via SMTP or prints to terminal if dry_run is True."""
    if not editais:
        print("[Notifier] Nenhum edital novo para enviar.")
        return True

    from jinja2 import Template
    date_str = datetime.now().strftime("%d/%m/%Y")
    template = Template(EMAIL_HTML_TEMPLATE)
    html_content = template.render(editais=editais, date_str=date_str)

    if dry_run:
        print("\n================ [PRÉ-VIEW DO E-MAIL (DRY RUN)] ================")
        print(f"Para: {Config.NOTIFY_EMAIL}")
        print(f"Assunto: 🎓 {len(editais)} Nova(s) Bolsa(s) de Capacitação em TI Encontrada(s)!")
        print("----------------------------------------------------------------")
        for item in editais:
            print(f"• {item['title']}")
            print(f"  Bolsa: {item['stipend_info']}")
            print(f"  Tópicos: {', '.join(item['topics'])}")
            print(f"  URL: {item['url']}\n")
        print("=================================================================\n")
        return True

    missing_configs = Config.validate()
    if missing_configs:
        print(f"[Notifier] Erro ao enviar e-mail. Variáveis ausentes: {', '.join(missing_configs)}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🎓 {len(editais)} Nova(s) Bolsa(s) de Capacitação em TI Encontrada(s)!"
        msg["From"] = Config.SMTP_USER
        msg["To"] = Config.NOTIFY_EMAIL

        part_html = MIMEText(html_content, "html", "utf-8")
        msg.attach(part_html)

        print(f"[Notifier] Conectando ao servidor SMTP {Config.SMTP_SERVER}:{Config.SMTP_PORT}...")
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_USER, Config.NOTIFY_EMAIL, msg.as_string())
        
        print(f"[Notifier] E-mail enviado com sucesso para {Config.NOTIFY_EMAIL}!")
        return True
    except Exception as e:
        print(f"[Notifier] Falha crítica ao enviar e-mail via SMTP: {e}")
        return False
