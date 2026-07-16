# ruff: noqa: INP001
"""Behavior tests for voice-enrich plugin."""

from __future__ import annotations

import sys
from importlib import util
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock

import pytest

from mindroom.hooks.decorators import get_hook_metadata


def _load_hooks_module() -> ModuleType:
    hooks_path = Path(__file__).resolve().parents[1] / "hooks.py"
    module_name = "mindroom_test_voice_enrich_hooks"
    spec = util.spec_from_file_location(module_name, hooks_path)
    assert spec is not None
    assert spec.loader is not None
    module = util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


hooks = _load_hooks_module()


def _context(body: str) -> SimpleNamespace:
    return SimpleNamespace(
        envelope=SimpleNamespace(body=body),
        add_metadata=MagicMock(),
    )


def test_hook_metadata_targets_message_enrichment() -> None:
    """Voice annotation should remain a lightweight enrichment hook."""
    metadata = get_hook_metadata(hooks.voice_enrich)

    assert metadata is not None
    assert metadata.event_name == "message:enrich"
    assert metadata.hook_name == "voice-enrich"
    assert metadata.timeout_ms == 200


@pytest.mark.asyncio
async def test_voice_transcript_adds_volatile_metadata() -> None:
    """Transcribed audio should carry model-facing uncertainty guidance."""
    ctx = _context(f"{hooks.VOICE_PREFIX}possible transcription")

    result = await hooks.voice_enrich(ctx)

    assert result == []
    ctx.add_metadata.assert_called_once_with(
        "voice_transcription",
        hooks.NOTE_TEXT,
        cache_policy="volatile",
    )


def test_note_text_explains_transcription_fallback() -> None:
    """Voice guidance should identify the source and recovery option."""
    assert "Whisper" in hooks.NOTE_TEXT
    assert "transcribe" in hooks.NOTE_TEXT


@pytest.mark.asyncio
async def test_plain_text_is_ignored() -> None:
    """Ordinary messages should not receive voice metadata."""
    ctx = _context("ordinary text")

    result = await hooks.voice_enrich(ctx)

    assert result == []
    ctx.add_metadata.assert_not_called()
