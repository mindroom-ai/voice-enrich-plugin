"""Voice transcription enrichment hook."""

from __future__ import annotations

from mindroom.constants import VOICE_PREFIX
from mindroom.hooks import EnrichmentItem, MessageEnrichContext, hook

NOTE_TEXT = """This message was transcribed from audio by Whisper. Treat the text as approximate:
- Homophone errors are common (e.g. "Cinny" -> "CINE"/"CINY", "claude.md" -> "clod.md").
- Proper nouns and rare technical terms are the most error-prone.
- Punctuation and casing reflect Whisper output, not the speaker's intent.
If a phrase looks semantically off or contains a clearly wrong term, you can re-transcribe the original
audio attachment using the `transcribe` skill (Whisper primary, Gemini fallback) before responding."""


@hook(event="message:enrich", name="voice-enrich", timeout_ms=200)
async def voice_enrich(ctx: MessageEnrichContext) -> list[EnrichmentItem]:
    """Annotate voice-transcribed messages for the model without changing the event body."""
    if not ctx.envelope.body.startswith(VOICE_PREFIX):
        return []

    ctx.add_metadata("voice_transcription", NOTE_TEXT, cache_policy="volatile")
    return []


__all__ = ["NOTE_TEXT", "voice_enrich"]
