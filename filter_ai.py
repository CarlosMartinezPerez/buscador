import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional, List
from config import Config

class EditalEvaluation(BaseModel):
    is_valid: bool = Field(description="True se o edital for sobre programa de capacitação, residência ou bolsa de estudo na área de TI (Web, IA, ML, IoT, Embarcados, etc.) e oferecer bolsa de estudos/remuneração/estipêndio.")
    title: str = Field(description="Título claro e objetivo do edital ou programa.")
    topics: List[str] = Field(description="Principais tecnologias ou tópicos abordados (ex: IA, IoT, Embarcados, Web, ML).")
    has_scholarship: bool = Field(description="True se especifica a existência de bolsa de estudo, estipêndio ou auxílio financeiro.")
    stipend_info: str = Field(description="Valor ou resumo da bolsa/remuneração (ex: 'R$ 2.500/mês' ou 'Bolsa integral mencionada').")
    deadline: str = Field(description="Data limite de inscrição ou 'Não especificado'.")
    summary: str = Field(description="Resumo de 2 a 3 frases destacando o objetivo do programa, público-alvo e como se inscrever.")

def analyze_candidate_with_gemini(title: str, url: str, snippet: str, full_content: str = "") -> Optional[EditalEvaluation]:
    """Uses Gemini API to analyze candidate web page content and filter valid IT scholarship calls."""
    if not Config.GEMINI_API_KEY:
        print("[FilterAI] Erro: GEMINI_API_KEY não foi configurada.")
        return None

    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    
    text_to_analyze = f"Título da página: {title}\nURL: {url}\nResumo/Snippet: {snippet}\n\nConteúdo extraído da página:\n{full_content if full_content else snippet}"
    
    prompt = """Você é um especialista em analisar editais de TI, programas de capacitação tecnológica, residências de software e bolsas de estudo.
Analise a informação fornecida sobre uma página/edital e determine se atende aos critérios:

1. É um edital, programa de formação, residência tecnológica ou curso de capacitação em Tecnologia da Informação (IA, Machine Learning, IoT, Sistemas Embarcados, Desenvolvimento Web, Ciência de Dados, Engenharia de Software, etc.)?
2. Oferece bolsa de estudo, estipêndio mensal, auxílio financeiro ou remuneração para o participante?
3. O programa está com inscrições abertas ou foi anunciado para o ano atual/próximo?

Retorne estritamente um JSON de acordo com o esquema."""

    # Tenta modelos Flash atualizados do Gemini
    models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-2.5-flash-lite", "gemini-2.0-flash-lite"]
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, text_to_analyze],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=EditalEvaluation,
                    temperature=0.1
                )
            )
            if response.text:
                data = json.loads(response.text)
                return EditalEvaluation(**data)
        except Exception:
            continue
            
    print(f"[FilterAI] Falha ao analisar URL {url} com os modelos do Gemini.")
    return None
