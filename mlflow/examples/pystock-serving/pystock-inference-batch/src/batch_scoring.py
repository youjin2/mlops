import pandas as pd
import mlflow
import mlflow.pyfunc


if __name__ == "__main__":
    with mlflow.start_run(run_name="batch_scoring") as run:

        # retrieve the production model
        model_name = "training-model-pystock"
        stage = 'Production'
        model = mlflow.pyfunc.load_model(
            model_uri=f"models:/{model_name}/{stage}"
        )

        # read input dataset for inference
        data = pd.read_csv("./data/input.csv", header=None)
        print(data.head())
        print(data.shape)

        # run batch inference
        y_probas = model.predict(data)
        y_preds = [1 if y_proba > 0.5 else 0 for y_proba in y_probas]
        data[len(data.columns)] = y_preds

        # save results
        result = data
        result.to_csv("./data/output.csv", index=False, header=None)
