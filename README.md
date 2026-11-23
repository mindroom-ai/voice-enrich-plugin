# Voice Enrich

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/mindroom-ai/voice-enrich-plugin/actions/workflows/plugin-ci.yml/badge.svg)](https://github.com/mindroom-ai/voice-enrich-plugin/actions/workflows/plugin-ci.yml)
[![Docs](https://img.shields.io/badge/docs-plugins-blue)](https://docs.mindroom.chat/plugins/)
[![Hooks](https://img.shields.io/badge/docs-hooks-blue)](https://docs.mindroom.chat/hooks/)

<picture>
  <source media="(prefers-reduced-motion: no-preference)" srcset="https://raw.githubusercontent.com/mindroom-ai/mindroom/main/assets/logo/logo-mark-animated.svg" />
  <img src="https://raw.githubusercontent.com/mindroom-ai/mindroom/main/assets/logo/logo-mark.svg" alt="MindRoom Logo" align="right" width="120" />
</picture>

A [MindRoom](https://github.com/mindroom-ai/mindroom) hook plugin that quietly tells agents when a message was transcribed from voice audio, so they account for speech-to-text errors without changing the visible chat message.

- **Voice-only activation:** runs only on transcribed voice messages (prefixed with `🎤 `) and leaves ordinary text messages untouched.
- **Invisible to chat:** adds guidance only for the model during reasoning; the Matrix message body shown to users stays unchanged.
- **Zero config, zero I/O:** hooks-only with no plugin settings, agent tools, or network calls.

For every transcribed voice message, the plugin attaches this note to the model's prompt context:

```text
This message was transcribed from audio by Whisper. Treat the text as approximate:
- Homophone errors are common (e.g. "Cinny" -> "CINE"/"CINY", "claude.md" -> "clod.md").
- Proper nouns and rare technical terms are the most error-prone.
- Punctuation and casing reflect Whisper output, not the speaker's intent.
If a phrase looks semantically off or contains a clearly wrong term, you can re-transcribe the original
audio attachment using the `transcribe` skill (Whisper primary, Gemini fallback) before responding.
```

> The default note assumes Whisper transcription and references a `transcribe` skill. Edit `NOTE_TEXT` in [hooks.py](hooks.py) if your transcription setup differs.

## Quick start

```bash
mindroom plugins install voice-enrich-plugin
```

```yaml
plugins:
  - path: plugins/voice-enrich-plugin
```

No plugin settings or agent tools are required.

Update later with `mindroom plugins update voice-enrich-plugin` (updating replaces the installed plugin directory, so keep a copy of custom `NOTE_TEXT` edits or use a manual checkout).
Needs MindRoom v2026.11.180 or later (plugin API 1.0).

<details>
<summary><b>How it works</b></summary>

1. MindRoom transcribes an incoming voice message and prefixes the visible body with `VOICE_PREFIX` (`🎤 ` from `mindroom.plugin_api`).
2. On `message:enrich`, the `voice-enrich` hook (`200 ms` timeout) checks whether `ctx.envelope.body.startswith(VOICE_PREFIX)`. Non-voice messages return `[]` immediately.
3. For voice messages, the hook attaches `NOTE_TEXT` via `ctx.add_metadata("voice_transcription", NOTE_TEXT, cache_policy="volatile")` and returns `[]`.
4. The agent sees the `voice_transcription` metadata for the current turn while the visible Matrix event body remains unmodified, with no network or file I/O.

</details>

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `voice-enrich` | `message:enrich` | Add voice transcription guidance when the message body starts with `🎤 ` |
