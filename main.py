import argparse
import sys
from config import Config
import database
from searcher import search_web_candidates, fetch_page_content
from filter_ai import analyze_candidate_with_gemini
from notifier import send_notification_email

def main():
    parser = argparse.ArgumentParser(description="Buscador de Editais de Capacitação em TI com Bolsa")
    parser.add_argument("--dry-run", action="store_true", help="Executa a busca e analise com IA sem enviar e-mail real nem salvar no banco")
    parser.add_argument("--test-search", action="store_true", help="Testa apenas a coleta de links via web search")
    parser.add_argument("--test-email", action="store_true", help="Envia um e-mail de teste com dados ficticios")
    args = parser.parse_args()

    # Inicializa banco de dados
    database.init_db()

    if args.test_email:
        print("[Main] Testando envio de e-mail...")
        test_data = [{
            "title": "Edital de Teste - Residência em IA & Sistemas Embarcados",
            "stipend_info": "R$ 2.500/mês",
            "deadline": "30/08/2026",
            "topics": ["IA", "Sistemas Embarcados", "IoT"],
            "summary": "Este e um e-mail de teste para verificar as configuracoes do seu servidor SMTP.",
            "url": "https://github.com/carlos/buscador"
        }]
        send_notification_email(test_data, dry_run=args.dry-run)
        return

    print("🔍 [1/4] Pesquisando candidatos a editais na web...")
    candidates = search_web_candidates()
    print(f"➜ Encontradas {len(candidates)} páginas candidatas.")

    if args.test_search:
        print("\n--- Resultados Brutos da Busca ---")
        for idx, item in enumerate(candidates, 1):
            print(f"{idx}. {item['title']} - {item['url']}")
        return

    # Filtra as URLs que ja foram processadas em execucoes anteriores
    unseen_candidates = [c for c in candidates if not database.is_url_seen(c['url'])]
    print(f"➜ {len(unseen_candidates)} candidata(s) inédita(s) (não processadas anteriormente).")

    if not unseen_candidates:
        print("✅ Nenhuma novidade hoje. Finalizando.")
        return

    print("\n🤖 [2/4] Analisando conteúdo com Gemini AI...")
    valid_editais = []

    for idx, candidate in enumerate(unseen_candidates, 1):
        url = candidate['url']
        title = candidate['title']
        snippet = candidate['snippet']

        print(f" [{idx}/{len(unseen_candidates)}] Analisando: {title[:50]}...")
        
        # Busca conteudo da pagina para uma analise mais rica
        full_content = fetch_page_content(url)
        
        evaluation = analyze_candidate_with_gemini(title, url, snippet, full_content)
        
        if evaluation and evaluation.is_valid and evaluation.has_scholarship:
            print(f"   ✨ APROVADO! Bolsa: {evaluation.stipend_info}")
            edital_dict = {
                "url": url,
                "title": evaluation.title or title,
                "topics": evaluation.topics,
                "has_scholarship": evaluation.has_scholarship,
                "stipend_info": evaluation.stipend_info,
                "deadline": evaluation.deadline,
                "summary": evaluation.summary
            }
            valid_editais.append(edital_dict)
            
            # Se nao for dry-run, registra no banco
            if not args.dry_run:
                database.save_edital(
                    url=url,
                    title=evaluation.title or title,
                    topics=", ".join(evaluation.topics),
                    stipend=evaluation.stipend_info,
                    deadline=evaluation.deadline,
                    summary=evaluation.summary
                )
        else:
            print("   ❌ Não se enquadra nos critérios (Sem bolsa ou fora do tema).")
            
        import time
        time.sleep(1)

    print(f"\n📧 [3/4] Preparando notificação para {len(valid_editais)} edital(is) qualificado(s)...")
    if valid_editais:
        send_notification_email(valid_editais, dry_run=args.dry_run)
    else:
        print("ℹ️ Nenhum edital novo atendeu aos critérios hoje.")

    print("\n🎉 [4/4] Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
