"""FFmpeg video assembler â€” takes slides (image+audio) and outputs WebM."""
import subprocess, logging
logger = logging.getLogger(__name__)


def assemble_video(slides: list, output_path: str, width: int, height: int) -> bool:
    """
    slides: list of (img_path, audio_path, duration_sec)
    Returns True on success.
    """
    if not slides:
        return False

    n   = len(slides)
    cmd = ["ffmpeg", "-y"]

    # Add all image inputs
    for img_path, _, dur in slides:
        cmd += ["-loop", "1", "-t", f"{dur:.3f}", "-i", img_path]

    # Add all audio inputs
    for _, aud_path, _ in slides:
        cmd += ["-i", aud_path]

    # Build concat filter
    fparts  = "".join(f"[{i}:v][{n+i}:a]" for i in range(n))
    filt    = f"{fparts} concat=n={n}:v=1:a=1 [vr][a]; [vr] scale={width}:{height} [v]"

    cmd += [
        "-filter_complex", filt,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libvpx",
        "-quality", "realtime",
        "-cpu-used", "8",
        "-deadline", "realtime",
        "-threads", "0",
        "-b:v", "1200k",
        "-c:a", "libvorbis",
        "-q:a", "4",
        output_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=120)
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr[-500:].decode(errors='ignore')}")
            return False
        return True
    except subprocess.TimeoutExpired:
        logger.error("FFmpeg timed out!")
        return False
    except Exception as e:
        logger.error(f"FFmpeg exception: {e}")
        return False