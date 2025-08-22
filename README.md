# LLM Fallbacks

[![Python Package](https://github.com/bodencrouch/llm-fallbacks/actions/workflows/python-package.yml/badge.svg)](https://github.com/bodencrouch/llm-fallbacks/actions/workflows/python-package.yml)
[![Python Publish](https://github.com/bodencrouch/llm-fallbacks/actions/workflows/python-publish.yml/badge.svg)](https://github.com/bodencrouch/llm-fallbacks/actions/workflows/python-publish.yml)
[![Daily Config Update](https://github.com/bodencrouch/llm-fallbacks/actions/workflows/daily-config-update.yml/badge.svg)](https://github.com/bodencrouch/llm-fallbacks/actions/workflows/daily-config-update.yml)

A comprehensive Python library for managing fallback mechanisms for Large Language Model (LLM) API calls using the [LiteLLM](https://github.com/BerriAI/liteLLM) library. This library helps you handle API failures gracefully by providing alternative models to try when a primary model fails.

## Features

- **Comprehensive Model Management**: Access to thousands of LLM models across multiple providers
- **Intelligent Fallback Strategies**: Automatic fallback configuration based on model capabilities and cost
- **Cost Optimization**: Built-in cost calculation and model sorting by price and performance
- **Multi-Modal Support**: Support for chat, completion, embedding, vision, audio, and more model types
- **Provider Management**: Custom provider configuration and API key management
- **LiteLLM Integration**: Seamless integration with LiteLLM proxy for production deployments
- **GUI Interface**: Interactive model filtering and selection interface
- **Configuration Export**: Generate ready-to-use LiteLLM YAML configurations

## Installation

```bash
pip install llm-fallbacks
```

### Development Installation

```bash
git clone https://github.com/bodencrouch/llm-fallbacks.git
cd llm-fallbacks
pip install -e .
```

## Quick Start

### Download the repo

```bash
git clone https://github.com/th3w1zard1/llm_fallbacks.git
cd llm_fallbacks
uv sync
uv run src/tests/test_core.py
```

### Basic Usage

```python
from llm_fallbacks import get_chat_models, get_fallback_list

# Get all available chat models
chat_models = get_chat_models()

# Get fallback models for a specific model
fallbacks = get_fallback_list("gpt-4", model_type="chat")
print(f"Fallback models for GPT-4: {fallbacks}")
```

### Model Filtering

```python
from llm_fallbacks import filter_models

# Get free chat models only
free_models = filter_models(
    model_type="chat",
    free_only=True
)

# Get models with specific capabilities
vision_models = filter_models(
    model_type="chat",
    vision=True
)
```

### Cost Analysis Examples

Sort the models by cost:

```python
from llm_fallbacks import get_litellm_models, sort_models_by_cost_and_limits

# Get all models with cost information
models = get_litellm_models()

# Sort models by cost (cheapest first)
sorted_models = sort_models_by_cost_and_limits(models, free_only=True)
print(repr(sorted_models))
```

Calculate cost for a specific model:

```python
from llm_fallbacks import get_litellm_models, calculate_cost_per_token

model_spec = get_litellm_models()["gpt-5"]
cost_per_token = calculate_cost_per_token(model_spec)
print(f"Cost per token: ${cost_per_token:.6f}")
```

### Configuration Generation

```python
from llm_fallbacks.generate_configs import to_litellm_config_yaml

# Generate LiteLLM configuration
config = to_litellm_config_yaml(
    providers=[],  # Your custom providers
    free_only=True
)

# Save to YAML file
import yaml
with open("litellm_config.yaml", "w") as f:
    yaml.dump(config, f)
```

or run `generate_configs.py`:
```bash
uv run src/generate_configs.py
```

## Core Components

### 1. Model Management (`core.py`)

- **`get_litellm_models()`**: Retrieve all available LiteLLM models with specifications
- **`get_chat_models()`**: Get models supporting chat completion
- **`get_completion_models()`**: Get models supporting text completion
- **`get_embedding_models()`**: Get models supporting text embeddings
- **`get_vision_models()`**: Get models supporting vision tasks
- **`get_audio_models()`**: Get models supporting audio processing

### 2. Configuration (`config.py`)

- **Model Specifications**: Comprehensive model metadata including capabilities, costs, and limits
- **Provider Configuration**: Custom provider setup for private or specialized models
- **Fallback Strategies**: Intelligent fallback configuration based on model compatibility

### 3. Configuration Generation (`generate_configs.py`)

- **LiteLLM YAML Export**: Generate production-ready LiteLLM proxy configurations
- **Fallback Mapping**: Automatic fallback model assignment based on capabilities
- **Cost Optimization**: Prioritize models by cost and performance

### 4. Interactive Interface (`__main__.py`)

- **GUI Application**: Tkinter-based interface for model exploration (experimental)
- **Advanced Filtering**: Multiple filtering methods (regex, quantile, outlier detection)
- **Data Export**: Export filtered results to various formats

## Configuration Files

The library generates several configuration files that are stored in the `configs/` directory:

- **`litellm_config.yaml`**: Full LiteLLM configuration with all models
- **`litellm_config_free.yaml`**: Configuration with free models only
- **`all_models.json`**: Complete model database in JSON format
- **`free_chat_models.json`**: Free chat models only
- **`custom_providers.json`**: Custom provider configurations

These files are automatically updated daily at 12:00 AM UTC via GitHub Actions to ensure you always have the latest model information and configurations.

## Advanced Features

### Custom Provider Configuration

```python
from llm_fallbacks.config import CustomProviderConfig

custom_provider = CustomProviderConfig(
    name="my-custom-provider",
    base_url="https://api.myprovider.com",
    api_key="your-api-key",
    models=["custom-model-1", "custom-model-2"]
)
```

### Fallback Strategy Customization

```python
from llm_fallbacks.config import RouterSettings

router_settings = RouterSettings(
    allowed_fails=3,
    cooldown_time=30,
    fallbacks=[{"gpt-4": ["gpt-3.5-turbo", "claude-3-sonnet"]}]
)
```

## CLI Usage

### Interactive GUI

```bash
python -m llm_fallbacks
```

### Generate Configurations

```bash
python -m llm_fallbacks.generate_configs
```

### System Testing

```bash
python test_system.py
```

## Development

### Prerequisites

- Python 3.12+
- Poetry or pip for dependency management

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

## CI/CD

The project includes automated workflows:

- **Python Package**: Runs on every push/PR with linting, testing, and building
- **Python Publish**: Automatically publishes to PyPI on releases
- **Daily Config Update**: Updates model configurations daily at 12:00 AM UTC

### Automated Configuration Updates

The library automatically maintains up-to-date model configurations through:

1. **Daily Updates**: GitHub Actions workflow runs every day at 12:00 AM UTC
2. **Model Database**: Fetches latest model information from LiteLLM
3. **Fallback Strategies**: Generates intelligent fallback configurations
4. **Version Control**: All changes are automatically committed and tracked

This ensures your applications always have access to the latest models, pricing, and capabilities without manual intervention.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Business Source License 1.1 (BSL 1.1) - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:

- Open an issue on GitHub
- Check the [documentation](https://github.com/bodencrouch/llm-fallbacks)
- Contact: boden.crouch@gmail.com

## Acknowledgments

- Built on top of [LiteLLM](https://github.com/BerriAI/liteLLM)
- Inspired by the need for robust LLM fallback strategies
- Community contributions and feedback

---

**Note**: This library is designed to work with the LiteLLM ecosystem and provides fallback mechanisms for production LLM applications. Always test fallback configurations in your specific environment before deploying to production.
