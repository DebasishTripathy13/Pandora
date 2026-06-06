"""Unit tests for pandora.core.config"""

from pandora.core.config import PandoraConfig, load_config


class TestPandoraConfig:
    def test_default_values(self):
        config = PandoraConfig()
        assert config.debug is False

    def test_llm_defaults(self):
        config = PandoraConfig()
        assert config.llm.proxy_url == "http://localhost:4000"
        assert config.llm.proxy_api_key == "sk-pandora-master"

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("PANDORA_DEBUG", "true")
        config = PandoraConfig()
        assert config.debug is True


class TestLoadConfig:
    def test_returns_defaults(self):
        config = load_config()
        assert config.llm.proxy_url == "http://localhost:4000"
        assert config.docker.sandbox_container_name == "pandora-sandbox"
