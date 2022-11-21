import io
import requests
import base64
import json

import streamlit as st


def predict(image_buffer: bytes, endpoint: str):
    """
    This function sends a prediction request to the API serer and return a cuteness score.
    """

    # send the image to the API
    response = requests.post(
        endpoint,
        headers={"content-type": "text/plain"},
        data=base64.b64encode(image_buffer),
    )

    if response.status_code == 200:
        score = float(json.loads(response.text)[0])
        return score
    else:
        raise Exception("Status: {}".format(response.status_code))


def predict_ui(image_file: io.BufferedReader, endpoint: str):
    """
    A web component returning a cuteness score of the given image.
    """

    image_buffer = image_file.read()
    with st.spinner("Predicting..."):
        pred_score = predict(
            image_buffer=image_buffer,
            endpoint=endpoint,
        )
        st.success(f"Your pet's cuteness score is {pred_score:0.3f}")
