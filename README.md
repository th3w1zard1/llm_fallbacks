# LLM Fallbacks

[![PyPI version](https://badge.fury.io/py/llm-fallbacks.svg)](https://badge.fury.io/py/llm-fallbacks)
[![Python Versions](https://img.shields.io/pypi/pyversions/llm-fallbacks.svg)](https://pypi.org/project/llm-fallbacks/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for managing fallbacks for LLM API calls using the [LiteLLM](https://github.com/BerriAI/litellm) library.

## Features

- 🔄 **Automatic Fallbacks**: Gracefully handle API failures by providing alternative models
- 📊 **Model Filtering**: Filter models based on various criteria like cost, context length, and capabilities
- 💰 **Cost Optimization**: Sort models by cost to optimize your API usage
- 🧠 **Model Discovery**: Discover available models and their capabilities
- 🛠️ **GUI Tool**: Includes a GUI tool for exploring and filtering available models

## Installation

```bash
pip install llm-fallbacks
```

## Quick Start

```python
from llm_fallbacks import get_chat_models, filter_models, get_fallback_list

# Get all available chat models
chat_models = get_chat_models()
print(f"Found {len(chat_models)} chat models")

# Filter models based on criteria
vision_models = filter_models(
    model_type="chat",
    supports_vision=True,
    max_cost_per_token=0.001
)
print(f"Found {len(vision_models)} vision-capable models under 0.001 per token")

# Get a fallback list for a specific model type
fallbacks = get_fallback_list("chat")
print(f"Recommended fallback order: {fallbacks}")
```

## GUI Tool

LLM Fallbacks includes a GUI tool for exploring and filtering available models:

```bash
# Run the GUI tool
python -m llm_fallbacks
```

## API Reference

### Core Functions

- `get_chat_models()`: Get all available chat models
- `get_completion_models()`: Get all available completion models
- `get_embedding_models()`: Get all available embedding models
- `get_image_generation_models()`: Get all available image generation models
- `get_audio_transcription_models()`: Get all available audio transcription models
- `get_audio_speech_models()`: Get all available audio speech models
- `get_moderation_models()`: Get all available moderation models
- `get_rerank_models()`: Get all available rerank models
- `get_vision_models()`: Get all available vision models
- `get_function_calling_models()`: Get all available function calling models
- `get_parallel_function_calling_models()`: Get all available parallel function calling models
- `get_image_input_models()`: Get all available image input models
- `get_audio_input_models()`: Get all available audio input models
- `get_audio_output_models()`: Get all available audio output models
- `get_pdf_input_models()`: Get all available PDF input models
- `get_models()`: Get all available models
- `get_fallback_list(model_type)`: Get a fallback list for a specific model type
- `filter_models(model_type, **kwargs)`: Filter models based on various criteria

### Filtering Models

The `filter_models` function allows you to filter models based on various criteria:

```python
from llm_fallbacks import filter_models

# Get free chat models that support vision
free_vision_models = filter_models(
    model_type="chat",
    free_only=True,
    supports_vision=True
)

# Get models with a minimum context length
long_context_models = filter_models(
    model_type="chat",
    min_context_length=16000
)

# Get models from a specific provider
openai_models = filter_models(
    model_type="chat",
    provider="openai"
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
