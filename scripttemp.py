from soundapi import button

genre_predicted, artist_name, track_name = button('record.wav')

print(genre_predicted, artist_name, track_name)
