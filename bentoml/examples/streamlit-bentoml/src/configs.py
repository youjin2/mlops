import os


# set project root directory
cur_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(cur_path))


# mlflow configs
mlflow_credential_path = os.path.join(parent_dir, "credentials.json")


# csv metadata path
train_meta_path = os.path.join(parent_dir, "petfinder/data/raw/train.csv")
test_meta_path = os.path.join(parent_dir, "petfinder/data/raw/test.csv")
