# -*- coding: utf-8 -*-
"""Untitled9.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I5PAxA2S6XoiwC-Pm2IbyYFf6VhqTkps
"""

import streamlit as st
import numpy as np
import librosa
import librosa.display
import cv2
import os
import tempfile
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

model = load_model("emotion_cnn_model.h5")
img_size = (128, 128)
emotion_labels = ['angry', 'calm', 'disgust', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

def audio_to_spectrogram(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    fig = plt.figure(figsize=(2.56, 2.56), dpi=50)  # 128x128 pixels
    ax = fig.add_subplot(111)
    ax.axis('off')
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max), sr=sr)

    tmp_img_path = os.path.join(tempfile.gettempdir(), "temp_spec.png")
    plt.savefig(tmp_img_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    img = cv2.imread(tmp_img_path)
    img = cv2.resize(img, img_size)
    img = img / 255.0
    return np.expand_dims(img, axis=0)

st.title("🎵 Speech Emotion Recognition App")
st.write("Upload a `.wav` audio file and the model will predict the **emotion**.")

uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        tmp_wav.write(uploaded_file.read())
        tmp_wav_path = tmp_wav.name

    st.audio(uploaded_file, format='audio/wav')
    st.write("Generating spectrogram...")

    input_img = audio_to_spectrogram(tmp_wav_path)
    prediction = model.predict(input_img)
    predicted_label = np.argmax(prediction)
    confidence = np.max(prediction)

    st.success(f"**Predicted Emotion:** {emotion_labels[predicted_label]}")
    st.info(f"Confidence: {confidence * 100:.2f}%")
    st.image(input_img[0], caption="Spectrogram", use_column_width=True)