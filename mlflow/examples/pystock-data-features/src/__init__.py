import os

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, "data")
os.makedirs(os.path.join(data_dir, "raw"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "staging"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "training"), exist_ok=True)
