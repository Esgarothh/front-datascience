from tokenize import Name
from webbrowser import get
import pyaudio
import wave
import subprocess
import random
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from urllib.request import urlretrieve
from red import predecir


<<<<<<< HEAD
def button(filename):
    sp = authenticate_spotify()
    record_audio(filename)
    output = execute_recognition_command(filename)
    genre_predicted = predecir('jazz1.wav')
    if output:
        artist_name, track_name = extract_artist_and_track(output)
        print(track_name)
        genero = search_and_download_preview(sp, track_name)
        if not genero:
            genre_predicted, artist_name, track_name = genRandomGenre(), "Artist Name", "Track_Name"
            print(genre_predicted)
            return genre_predicted, artist_name, track_name
        genre_predicted = genero
        return genre_predicted, artist_name, track_name
        genre_predicted, artist_name, track_name = genRandomGenre(), "Artist Name", "Track_Name"
        print(genre_predicted)
        return genre_predicted, artist_name, track_name
    else:
        genre_predicted, artist_name, track_name = genRandomGenre(), "Artist Name", "Track_Name"
        print(genre_predicted)
        return genre_predicted, artist_name, track_name
        #print("No se pudo reconocer la canción.")
    # print(artist_name)
    # print(track_name)
    return genre_predicted, artist_name, track_name


def authenticate_spotify():
    return Spotify(
        auth_manager=SpotifyOAuth(
            client_id="123",
            client_secret="123",
            redirect_uri="http://localhost:1234",
            scope="user-library-read",
        )
    )
# Grabar
=======
>>>>>>> origin/main


def record_audio(filename, seconds=10, chunk=1024, sample_format=pyaudio.paInt16,
                 channels=2, fs=44100):
    """
    Records audio from the default audio input device and saves it to a file.

    Args:
        filename (str): The name of the file to save the recorded audio to.
        seconds (int, optional): The duration of the recording in seconds. Defaults to 10.
        chunk (int, optional): The number of audio frames per buffer. Defaults to 1024. 
        sample_format (int, optional): The format of the audio samples. Defaults to pyaudio.paInt16.
        channels (int, optional): The number of audio channels. Defaults to 2.
        fs (int, optional): The sample rate of the audio. Defaults to 44100.

    Returns:
        None
    """
    p = pyaudio.PyAudio()

    print('Por favor espere, ¡Grabación en proceso!')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    print('Grabación completada.')

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

# Reconocer


def execute_recognition_command(filename):
    """
    Executes a recognition command for the given filename.

    Args:
        filename (str): The name of the file to be recognized.

    Returns:
        str or None: The output of the recognition command if successful, None otherwise.
    """
    command = f"songrec recognize {filename}"

    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        print("Error executing the command:", e)
        return None

# Split


def extract_artist_and_track(output):
    """
    Extracts the artist and track from the given output.

    Parameters:
        output (str): The output string containing the artist and track separated by a hyphen and a space.

    Returns:
        tuple: A tuple containing the artist and track extracted from the output. If the output is empty, returns (None, None).
    """
    if output:
        parts = output[:-1].split(" - ")
        return parts[0], parts[1]

    return None, None

# Extraer


def search_and_download_preview(sp, track_name):
    """
    Search and download a preview of a track.

    Args:
        sp (Spotify): An instance of the Spotify class.
        track_name (str): The name of the track to search for.

    Returns:
        None
    """
    try:
        results = sp.search(track_name, type="track")
        preview_url = results["tracks"]["items"][0]["preview_url"]
        preview_file = f'./wav/{results["tracks"]["items"][0]["name"]}.wav'

        # print(preview_url)
        if preview_url:
            urlretrieve(preview_url, preview_file)
        else:
            # print("No se pudo encontrar ninguna previsualización.")
            artist_id = results["tracks"]["items"][0]["artists"][0]["id"]
            results2 = sp.artist(artist_id)
            if results2:
                print(results2["genres"][0])
                return results2["genres"][0]
            else:
                print("No genres available.")
    except NameError:
        print(NameError)
        return False


def genRandomGenre():
    genres = {'jazz', 'hiphop', 'reggae', 'country', 'pop',
              'metal', 'classical', 'disco', 'blues', 'rock'}
    genre = random.choice(list(genres))
    return genre
