
from tkinter import N
from flask import Flask, render_template, request
from soundapi import button
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/record', methods=['GET'])
def record():

    genre_predicted = None
    while not genre_predicted:
        genre_predicted, artist_name, track_name = button('record.wav')

    # Your existing code for recording and recognizing the song
    # ...

    # Pass the song information to the template
    return render_template('result.html', artist=artist_name, track=track_name, genre_predicted=genre_predicted)


if __name__ == '__main__':
    app.run(debug=True)
