import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import os
import json
import math
import librosa

import IPython.display as ipd
import librosa.display

import tensorflow as tf


import sklearn.model_selection as sk

from sklearn.model_selection import train_test_split

JSON_PATH = "data_10.json"
SAMPLE_RATE = 22050
TRACK_DURATION = 30  # measured in seconds
SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION


def extract_features_from_wav(wav_path, num_mfcc=13, n_fft=2048, hop_length=512, num_segments=6):
    """
    Extracts MFCC features from a WAV file.

    :param wav_path (str): Path to the WAV file
    :param num_mfcc (int): Number of coefficients to extract
    # of samples
    :param n_fft (int): Interval we consider to apply FFT. Measured in
    :param hop_length (int): Sliding window for FFT. Measured in # of samples
    :param num_segments (int): Number of segments to divide the audio file into
    :return: List of MFCC features
    """
    desired_sample_rate = 22050  # Replace with the sample rate used during training
    desired_duration = 30
    # Load audio file and resample if necessary
    file_path = wav_path
    signal, current_sample_rate = librosa.load(file_path, sr=None)
    print("current sample rate of file = ", current_sample_rate)
    if current_sample_rate != desired_sample_rate:
        signal = librosa.resample(
            signal, orig_sr=current_sample_rate, target_sr=desired_sample_rate)

    current_duration = librosa.get_duration(y=signal, sr=desired_sample_rate)

    if current_duration < desired_duration:
        num_samples_to_pad = int(
            (desired_duration - current_duration) * desired_sample_rate)
        signal = np.pad(signal, (0, num_samples_to_pad), mode='constant')

    # list to store MFCC features
    features = []

    samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)

    signal, sample_rate = librosa.load(wav_path, sr=SAMPLE_RATE)
    print("signal:", signal, "sample_rate_new=", sample_rate)
    # process all segments of audio file
    for d in range(num_segments):
        # calculate start and finish sample for the current segment
        start = samples_per_segment * d
        finish = start + samples_per_segment

        # extract mfcc
        mfcc = librosa.feature.mfcc(
            y=signal[start:finish], sr=sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)

        # store only mfcc feature with the expected number of vectors
        if len(mfcc.T) == num_mfcc_vectors_per_segment:
            features.append(np.expand_dims(mfcc.T, axis=-1))

    return features


def predict_one(model, X, y):
    """Predict a single sample using the trained model
    :param model: Trained classifier
    :param X: Input data
    :param y (int): Target
    """

    # add a dimension to input data for sample - model.predict() expects a 4d array in this case

    X = X[np.newaxis, ...]  # array shape (1, 130, 13, 1)

    # perform prediction
    prediction = model.predict(X)

    # get index with max value
    predicted_index = np.argmax(prediction, axis=1)
    z = ['jazz', 'metal', 'classical', 'pop', 'disco', 'hiphop', 'blues', 'country',
         'rock', 'reggae']
    # get mappings for target and predicted label
    target = z[y]
    predicted = z[predicted_index[0]]

    print("Target: {}, Predicted label: {}".format(target, predicted))
    return predicted


new_wav_path_1 = '/content/gtzan-dataset-music-genre-classification/Data/predecir/parapredecir/stayingAlive.wav'


def predecir(filepath):

    new_model = tf.keras.models.load_model('my_model.h5')
    extracted_features = extract_features_from_wav(filepath)

    return predict_one(new_model, extracted_features[0], 0)
