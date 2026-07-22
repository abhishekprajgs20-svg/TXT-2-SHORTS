"""
Audio generation:
- generate_speech()  â†’ edge-tts (Microsoft Azure, free, no API key)
- generate_ticking_wav() â†’ pure Python math (no deps)
- generate_silent_wav()  â†’ pure Python
"""
import wave, math, struct, asyncio
import edge_tts


VOICE = "en-US-GuyNeural"   # Free Microsoft Azure TTS voice


async def generate_speech(text: str, output_path: str, voice: str = VOICE):
    """Generate speech MP3 using edge-tts (Microsoft free TTS)."""
    if not text or not text.strip():
        text = "."
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
    except Exception as e:
        # Fallback: generate silence if TTS fails
        generate_silent_wav(output_path.replace(".mp3", ".wav"), 2.0)


def generate_ticking_wav(filepath: str, duration_sec: float = 10.0, sample_rate: int = 44100):
    """Pure-math loud crisp clock ticking WAV â€” no external deps."""
    n = int(sample_rate * duration_sec)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sample_rate)
        for i in range(n):
            t  = i / float(sample_rate)
            sf = t - math.floor(t)
            tick = 0.0
            if sf < 0.048:
                freq = 1500.0 if int(t) % 2 == 0 else 1100.0
                env  = math.exp(-sf * 110.0)
                tick = 0.82 * math.sin(2 * math.pi * freq * t) * env
                tick+= 0.55 * math.sin(2 * math.pi * freq * 0.5 * t) * env
            drone = 0.07 * math.sin(2 * math.pi * 120.0 * t)
            s = max(-1.0, min(1.0, tick + drone))
            wf.writeframes(struct.pack('<h', int(s * 32767)))


def generate_silent_wav(filepath: str, duration_sec: float = 1.0, sample_rate: int = 44100):
    n = int(sample_rate * duration_sec)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sample_rate)
        wf.writeframes(b'\x00\x00' * n)