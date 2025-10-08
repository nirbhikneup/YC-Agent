"""Utility helpers for interacting with Hugging Face hosted LLaMA models."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import pandas as pd

try:
    from huggingface_hub import InferenceClient
except ImportError as exc:  # pragma: no cover - handled at runtime
    InferenceClient = None  # type: ignore
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


DEFAULT_MODEL_ID = os.getenv(
    "HUGGINGFACE_MODEL_ID", "meta-llama/Meta-Llama-3-80B-Instruct"
)
DEFAULT_SYSTEM_PROMPT = os.getenv(
    "LLM_SYSTEM_PROMPT",
    (
        "You are an expert analyst helping surface insights about YC companies. "
        "Use the provided context to answer questions accurately and cite data-driven observations."
    ),
)


class LLMConfigurationError(RuntimeError):
    """Raised when the LLM configuration is invalid."""


@lru_cache(maxsize=1)
def _get_client(model_id: str, token: str) -> InferenceClient:
    if InferenceClient is None:
        raise LLMConfigurationError(
            "huggingface_hub is not installed. Please add 'huggingface-hub' to your dependencies."
        ) from _IMPORT_ERROR
    return InferenceClient(model=model_id, token=token)


def build_dataset_context(df: Optional[pd.DataFrame], max_items: int = 5) -> str:
    """Create a concise text summary of the dataset for the language model."""
    if df is None or df.empty:
        return ""

    sections: list[str] = []
    total_companies = len(df)
    sections.append(f"Total companies in dataset: {total_companies}.")

    if "batch" in df.columns:
        top_batches = df["batch"].value_counts().head(max_items)
        if not top_batches.empty:
            formatted_batches = ", ".join(
                f"{batch} ({count})" for batch, count in top_batches.items()
            )
            sections.append(f"Most represented batches: {formatted_batches}.")

    if "industry" in df.columns:
        top_industries = df["industry"].value_counts().head(max_items)
        if not top_industries.empty:
            formatted_industries = ", ".join(
                f"{industry} ({count})" for industry, count in top_industries.items()
            )
            sections.append(f"Top industries: {formatted_industries}.")

    if "email_count" in df.columns:
        avg_emails = df["email_count"].mean()
        max_emails = df["email_count"].max()
        sections.append(
            f"Average email count per company: {avg_emails:.2f}. Highest email count: {int(max_emails)}."
        )

        top_email_companies = df.nlargest(min(max_items, len(df)), "email_count")
        company_snippets = ", ".join(
            f"{row['name']} ({row['email_count']} emails{', ' + row['batch'] if 'batch' in row else ''})"
            for _, row in top_email_companies.iterrows()
        )
        sections.append(f"Companies with the most emails: {company_snippets}.")

    if "valuation" in df.columns:
        top_valuations = df.nlargest(min(max_items, len(df)), "valuation")
        valuation_snippets = ", ".join(
            f"{row['name']} (${row['valuation']:,})" for _, row in top_valuations.iterrows()
        )
        sections.append(f"Highest valuations: {valuation_snippets}.")

    return "\n".join(sections)


def generate_llama3_response(prompt: str, context: Optional[str] = None) -> str:
    """Call the configured Hugging Face LLaMA 3 model and return the response text."""
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not token:
        raise LLMConfigurationError(
            "HUGGINGFACE_API_TOKEN environment variable is not set."
        )

    model_id = os.getenv("HUGGINGFACE_MODEL_ID", DEFAULT_MODEL_ID)
    client = _get_client(model_id, token)

    user_prompt = prompt if not context else f"{prompt}\n\nContext:\n{context}"

    try:
        completion = client.chat_completion(
            messages=[
                {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=float(os.getenv("LLM_TEMPERATURE", 0.2)),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", 512)),
            top_p=float(os.getenv("LLM_TOP_P", 0.9)),
        )
    except Exception as exc:  # pragma: no cover - network errors
        raise RuntimeError(f"Failed to contact Hugging Face Inference API: {exc}") from exc

    choices = getattr(completion, "choices", None)
    if not choices:
        raise RuntimeError("No completion choices returned by the Hugging Face Inference API.")

    message = choices[0].message
    if isinstance(message, dict):
        content = message.get("content")
    else:
        content = getattr(message, "content", None)

    if isinstance(content, list):
        text_chunks: list[str] = []
        for chunk in content:
            if isinstance(chunk, dict):
                text = chunk.get("text")
                if text:
                    text_chunks.append(str(text))
            elif isinstance(chunk, str):
                text_chunks.append(chunk)
        content = "\n".join(text_chunks).strip() if text_chunks else None
    elif isinstance(content, str):
        content = content.strip()
    elif content is not None:
        content = str(content).strip()

    if not content:
        raise RuntimeError("Empty response received from the Hugging Face Inference API.")

    return content
