# Voice Enrich

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-plugins-blue)](https://docs.mindroom.chat/plugins/)
[![Hooks](https://img.shields.io/badge/docs-hooks-blue)](https://docs.mindroom.chat/hooks/)

<img src="https://media.githubusercontent.com/media/mindroom-ai/mindroom/refs/heads/main/frontend/public/logo.png" alt="MindRoom Logo" align="right" width="120" />

AI-only enrichment for [MindRoom](https://github.com/mindroom-ai/mindroom) voice messages.

When a transcribed voice message arrives, this plugin silently injects a note into the agent prompt explaining that the text came from speech recognition and may contain transcription mistakes. The user-facing Matrix event body is never modified.

## Features

- Detects voice-origin messages using `mindroom.constants.VOICE_PREFIX` (`🎤 `)
- Injects AI-only metadata via `MessageEnrichContext.add_metadata`
- Warns about common speech-to-text failure modes such as homophones, proper nouns, and rare technical terms
- Suggests re-transcribing the original audio attachment when the transcript looks garbled
- Zero-config, hooks-only behavior
- Lightweight execution with no network or file I/O in the hook path

## How It Works

1. MindRoom transcribes an incoming voice message and prefixes the visible body with `🎤 `.
2. On `message:enrich`, the `voice-enrich` hook checks whether the incoming body starts with `VOICE_PREFIX`.
3. If it does, the hook adds a volatile `voice_transcription` metadata note to the prompt context.
4. The agent sees the note during reasoning, but the Matrix message body shown to the user stays unchanged.

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `voice-enrich` | `message:enrich` | Add voice transcription guidance when the message body starts with `🎤 ` |

## Setup

1. Copy this plugin to `~/.mindroom/plugins/voice-enrich`.
2. Add the plugin to `config.yaml`:
   ```yaml
   plugins:
     - path: plugins/voice-enrich
   ```
3. Restart MindRoom.

No agent tools or plugin settings are required. This plugin is hooks-only.
