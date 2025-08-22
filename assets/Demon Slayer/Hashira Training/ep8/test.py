import subprocess, math, glob, re

output_file = "index.m3u8"

# Lấy danh sách file ts trong thư mục hiện tại (vd: index001.ts, index002.ts ...)
ts_files = sorted(glob.glob("*.ts"))

segments = []
max_duration = 0

# Dò duration từng file bằng ffprobe
for ts_file in ts_files:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", ts_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    try:
        duration = float(result.stdout.strip())
    except:
        duration = 0.0

    segments.append((ts_file, duration))
    if duration > max_duration:
        max_duration = duration

# Ghi file index.m3u8
with open(output_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write("#EXT-X-VERSION:3\n")
    f.write(f"#EXT-X-TARGETDURATION:{math.ceil(max_duration)}\n")
    f.write("#EXT-X-MEDIA-SEQUENCE:0\n")

    for ts_file, duration in segments:
        f.write(f"#EXTINF:{duration:.3f},\n")
        f.write(f"{ts_file}\n")

    f.write("#EXT-X-ENDLIST\n")
