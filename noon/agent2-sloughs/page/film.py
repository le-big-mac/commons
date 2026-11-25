"""Put the film together: the frames written by film-river.js and the sound the page rendered for them.
usage: python -I film.py FRAMEDIR OUT.mp4 OUT.mp3"""
import sys, json, wave, subprocess, numpy as np
d, mp4, mp3 = sys.argv[1:4]; info = json.load(open(d + "/bells.json")); SR = 44100
raw = np.fromfile(d + "/sound.f32", "<f4"); n = len(raw) // 2; x = np.stack([raw[:n], raw[n:]], 1)
peak = float(np.abs(x).max()); fade = int(3 * SR); x[-fade:] *= np.linspace(1, 0, fade)[:, None]
w = wave.open(d + "/sound.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()); w.close()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", d + "/sound.wav", "-codec:a", "libmp3lame", "-q:a", "3", mp3], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(info["fps"]), "-i", d + "/f-%05d.jpg", "-i", d + "/sound.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
                "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], check=True)
print("film: %d s of frames at %d a second; sound %.1f s, peak %.3f of full scale; %d bells; hurried until %.2f s; time at the end %.2f; %d cutoffs" % (
    info["seconds"], info["fps"], n / SR, peak, len(info["strikes"]), info["hurriedUntil"], info["timeAtEnd"], info["cutoffs"]))
