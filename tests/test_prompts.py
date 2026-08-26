"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_FILE = str(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")


def load_prompts(file_path: str = PROMPT_FILE):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data = load_prompts()
        self.prompt_name = "bug_to_user_story_v2"
        assert self.prompt_name in self.data, f"Prompt '{self.prompt_name}' não encontrado no YAML"
        self.prompt = self.data[self.prompt_name]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt, "Campo 'system_prompt' não encontrado"
        system_prompt = self.prompt["system_prompt"]
        assert isinstance(system_prompt, str), "'system_prompt' deve ser uma string"
        assert len(system_prompt.strip()) > 0, "'system_prompt' não pode estar vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = self.prompt.get("system_prompt", "")
        role_keywords = ["você é um", "voce e um"]
        has_role = any(kw in system_prompt.lower() for kw in role_keywords)
        assert has_role, "O prompt deve definir uma persona/papel explícito (ex: 'Você é um Product Manager')"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt.get("system_prompt", "")
        format_keywords = ["user story", "markdown"]
        has_format = any(kw in system_prompt.lower() for kw in format_keywords)
        assert has_format, "O prompt deve especificar o formato de User Story ou markdown"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt.get("system_prompt", "")
        few_shot_keywords = ["exemplo", "exemplos"]
        matches = [kw for kw in few_shot_keywords if kw in system_prompt.lower()]
        assert len(matches) >= 2, "O prompt deve conter exemplos Few-shot com pares de entrada/saída"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        yaml_content = yaml.dump(self.prompt)
        assert "TODO" not in yaml_content, "O prompt contém pendências '[TODO]' que devem ser resolvidas"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt.get("techniques_applied") or []
        assert isinstance(techniques, list), "As técnicas aplicadas devem ser uma lista"
        assert len(techniques) >= 2, f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])