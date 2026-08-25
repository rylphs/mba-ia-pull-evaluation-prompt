"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()
PROMPT_ID = "leonanluppi/bug_to_user_story_v1"
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v1.yml"
client = Client()

def env_vars_are_all_set():
    """Verifica se as variáveis de ambiente necessárias estão definidas."""
    required_vars = ["LANGSMITH_API_KEY", "LANGSMITH_ENDPOINT", 
                     "LANGSMITH_PROJECT", "USERNAME_LANGSMITH_HUB"]
    return check_env_vars(required_vars)

def get_prompt_with_meta(prompt_id: str):
    """Obtém o prompt do LangSmith com metadados."""
    prompt_name = prompt_id.split("/")[-1]
    metadata = client.get_prompt(prompt_id)
    prompt = client.pull_prompt(prompt_id)
    system_prompt = prompt.messages[0].prompt.template
    user_prompt = prompt.messages[1].prompt.template
    return {prompt_name: {
        "description": metadata.description,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "tags": metadata.tags,
    }}
   

def pull_prompts_from_langsmith():
    prompt = get_prompt_with_meta(PROMPT_ID)
    save_yaml(prompt, PROMPT_PATH)
    return prompt


def main():
    """Função principal"""
    if not env_vars_are_all_set():
        sys.exit(1)
    print_section_header("Obtendo o prompt e salvando localmente...")
    pull_prompts_from_langsmith()
    print(f"Prompt salvo em {PROMPT_PATH}")


if __name__ == "__main__":
    sys.exit(main())
