
from flask import Flask, render_template, request
from soundapi import button
app = Flask(__name__)

items = [
    {'cancion': 'Song 1', 'genero_predicho': 'Pop',
     'genero_real': 'Pop'}
]


@app.route('/')
def index():
    
    artist = "artista"
    track = "cancion"
    genre_predicted = "genero"

    return render_template('index.html', artist=artist, track=track, genre_predicted=genre_predicted, items=items)


@app.route('/test', methods=['GET'])
def test():
    return render_template('result.html')


@app.route('/record', methods=['GET'])
def record():

    genre_predicted, artist_name, track_name, real_genre = button(
        'record.wav')

    if genre_predicted == real_genre:
        intento = {'cancion': track_name, "genero_predicho": genre_predicted,
                   "genero_real": real_genre}
    else:
        intento = {'cancion': track_name, "genero_predicho": genre_predicted,
                   "genero_real": real_genre}
    items.append(intento)

    # Your existing code for recording and recognizing the song
    # ...

    # Pass the song information to the template
    return render_template('result.html', artist=artist_name, track=track_name, genre_predicted=genre_predicted, genre=real_genre, items=items)


if __name__ == '__main__':
    app.run(debug=True)
