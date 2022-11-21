import streamlit as st

from utils import predict_ui


API_ENDPOINT = "http://0.0.0.0:3000/predict_text"
# API_ENDPOINT = "https://youjin2-pet-pawpularity.herokuapp.com/predict_text"


st.title("Pet Pawpularity Prediction App")
st.markdown(
    "### Predict the cuteness score of your cat or dog with machine learning",
    unsafe_allow_html=True,
)

# upload a simple cover image
with open("./doc/figures/app_cover.jpg", "rb") as f:
    st.image(f.read(), use_column_width=True)

st.markdown("### Grab a picture of your pet or upload an image to get a Pawpularity score.")


def main():
    image_file = st.file_uploader("Upload an image", type=["jpg", "png"])
    if image_file is not None:
        predict_ui(image_file=image_file, endpoint=API_ENDPOINT)

    camera_input = st.camera_input("Or take a picture")
    if camera_input is not None:
        predict_ui(image_file=image_file, endpoint=API_ENDPOINT)


if __name__ == "__main__":
    main()
