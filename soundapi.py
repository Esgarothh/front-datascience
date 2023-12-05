import pyaudio
import wave
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.request import urlretrieve



chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100
seconds = 10
filename = "miley.wav"

p = pyaudio.PyAudio()

print('Please wait. Recording in progress.')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []

for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

stream.stop_stream()
stream.close()

p.terminate()

print('Finished recording.')

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

command = f"songrec recognize {filename}"

try:
    output = subprocess.check_output(command, shell=True, text=True)
    #print("Respuesta:", output)
except subprocess.CalledProcessError as e:
    print("Error al ejecutar el comando:", e)

artist_name = output.split(" - ")[0]
track_name = output[:-1].split(" - ")[1]

# print(output[:-1])
# print(len(output[:-1]))
print(artist_name)
print(track_name)

results = sp.search(track_name, type="track")
preview_url = results["tracks"]["items"][0]["preview_url"]
preview_file = f'{results["tracks"]["items"][0]["name"]}.mp3'

print(preview_url)

urlretrieve(preview_url, preview_file)
