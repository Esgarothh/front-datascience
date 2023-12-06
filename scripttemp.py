from soundapi import button

genre_predicted, artist_name, track_name, real_genre = button('record.wav')

print(genre_predicted, artist_name, track_name, real_genre)
