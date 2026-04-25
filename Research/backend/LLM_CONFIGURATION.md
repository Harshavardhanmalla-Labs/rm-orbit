# Research Backend LLM Configuration

The backend uses one OpenAI-compatible LLM interface for the full paper pipeline.
Ollama is the default local provider, but external API providers can be used by
changing environment variables.

## Local Ollama Default

```bash
export RESEARCH_LLM_PROVIDER=ollama
export RESEARCH_LLM_MODEL=gemma4:e4b
export RESEARCH_LLM_BASE_URL=http://localhost:11434/v1
export RESEARCH_LLM_API_KEY=ollama
```

## External API Provider

For an OpenAI-compatible API, set:

```bash
export RESEARCH_LLM_PROVIDER=openai
export RESEARCH_LLM_MODEL=<model-name>
export RESEARCH_LLM_API_KEY=<api-key>
```

If the provider uses a custom OpenAI-compatible endpoint:

```bash
export RESEARCH_LLM_BASE_URL=https://provider.example.com/v1
```

## Validation

Check provider readiness:

```bash
curl -sf http://localhost:6420/api/system/brain
```

Run a direct LLM smoke test:

```bash
curl -sf -X POST http://localhost:6420/api/system/llm/smoke
```

The pipeline refuses to start if the required LLM is not configured.
