# Voice Enrich

`voice-enrich` adds an AI-only note for messages that were transcribed from audio.
It runs on every `message:enrich` hook invocation.
When `ctx.envelope.body` starts with `VOICE_PREFIX` (`🎤 `), it adds prompt metadata explaining that Whisper output may contain transcription errors.
The note calls out homophones, proper nouns, and rare technical terms as the main failure modes.
It also tells the AI it can re-transcribe the original audio attachment with the `transcribe` skill if the text looks garbled or semantically off.

This plugin does not modify the Matrix event body.
Users still see exactly `🎤 <transcript>`.
