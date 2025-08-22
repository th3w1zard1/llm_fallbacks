from __future__ import annotations

from typing import TYPE_CHECKING

from importlib.util import find_spec

# import pytest


if __name__ == "__main__" and not find_spec("llm_fallbacks"):  # type: ignore[reportUnboundVariable]
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from llm_fallbacks import (
    get_chat_models,
    get_completion_models,
    get_embedding_models,
    get_fallback_list,
    filter_models,
)

if TYPE_CHECKING:
    from llm_fallbacks.config import LiteLLMBaseModelSpec


def test_get_chat_models():
    """Test that get_chat_models returns a dictionary."""
    models: dict[str, LiteLLMBaseModelSpec] = get_chat_models()
    assert isinstance(models, dict)
    print("✅ Passed test_get_chat_models")

def test_get_completion_models():
    """Test that get_completion_models returns a dictionary."""
    models: dict[str, LiteLLMBaseModelSpec] = get_completion_models()
    assert isinstance(models, dict)
    print("✅ Passed test_get_completion_models")

def test_get_embedding_models():
    """Test that get_embedding_models returns a dictionary."""
    models: dict[str, LiteLLMBaseModelSpec] = get_embedding_models()
    assert isinstance(models, dict)
    print("✅ Passed test_get_embedding_models")

def test_get_fallback_list():
    """Test that get_fallback_list returns a list."""
    fallbacks: list[str] = get_fallback_list("chat")
    assert isinstance(fallbacks, list)
    print("✅ Passed test_get_fallback_list")

def test_filter_models():
    """Test that filter_models returns a list."""
    models: list[str] = filter_models(model_type="chat")
    assert isinstance(models, list)
    print("✅ Passed test_filter_models")

def test_filter_models_with_criteria():
    """Test that filter_models with criteria returns a list."""
    models: list[str] = filter_models(
        model_type="chat",
        free_only=True,
    )
    assert isinstance(models, list)
    print("✅ Passed test_filter_models_with_criteria")


if __name__ == "__main__":
    test_get_chat_models()
    test_get_completion_models()
    test_get_embedding_models()
    test_get_fallback_list()
    test_filter_models()
    test_filter_models_with_criteria()