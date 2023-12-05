
from flask import Flask, render_template, request

app = Flask(__name__)


# Your existing code for recording and recognizing the song
entorno = {
    "cancionesRock": 3}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/record', methods=['POST'])
def record():
    # Your existing code for recording and recognizing the song
    # ...

    # Pass the song information to the template
    return render_template('result.html', artist=artist_name, track=track_name, preview_url=preview_url)


if __name__ == '__main__':
    app.run(debug=True)
