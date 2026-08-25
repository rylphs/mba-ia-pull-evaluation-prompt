"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()
PROMPT_NAME = "bug_to_user_story_v2"
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
USER_HANDLE = os.getenv("USERNAME_LANGSMITH_HUB")

def generate_readme(description: str, techniques: list) -> str:
    """
    Gera o conteúdo do README.md com base nas técnicas aplicadas.

    Args:
        techniques: Lista de técnicas aplicadas

    Returns:
        Conteúdo do README.md
    """
    readme_content = f"## Descrição\n\n{description}\n\n"
    if not techniques:
        return readme_content
    readme_content += "## Técnicas Aplicadas\n\n"
    for technique in techniques:
        readme_content += f"- {technique}\n"
    return readme_content

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        client = Client()
        template = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data["user_prompt"]),
        ])
        tags = list(prompt_data.get("tags") or [])
        tecnicas = prompt_data.get("techniques") or []
        descricao = prompt_data.get("description") or ""
        url = client.push_prompt(
            prompt_identifier=f"{USER_HANDLE}/{prompt_name}",
            object=template,
            tags=tags,
            readme=generate_readme(descricao, tecnicas),
            description=descricao,
            is_public=True,
        )
        print(f"Prompt '{prompt_name}' enviado com sucesso para o LangSmith Hub: {url}")
        return True
    except Exception as e:
        print(f"Erro ao enviar o prompt '{prompt_name}': {e}")
        return False
    

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    ...


def main():
    """Função principal"""
    print_section_header("Validando e enviando o prompt para o LangSmith Hub...")
    required_vars = ["LANGSMITH_API_KEY", "LANGSMITH_ENDPOINT", 
                     "LANGSMITH_PROJECT", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        sys.exit(1)
    prompt_data = load_yaml(PROMPT_PATH)
    is_valid, errors = [True, []]
    if not is_valid:
        print("Prompt inválido. Erros encontrados:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    push_prompt_to_langsmith(PROMPT_NAME, prompt_data[PROMPT_NAME])


if __name__ == "__main__":
    sys.exit(main())
