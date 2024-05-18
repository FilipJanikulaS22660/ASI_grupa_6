import pandas as pd
import wandb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def evaluate_model(predictions_test: pd.DataFrame,
                   project_name='asi_grupa_6_autogluon',
                   learning_rate=0.01,
                   epochs=10) -> [pd.DataFrame, pd.DataFrame]:
    """
    Evaluate the model using various metrics and log results to Weights & Biases.

    Args:
        predictions_test (pd.DataFrame): DataFrame containing actual and predicted values of HeartDisease variable.
        project_name (str): Name of the W&B project. Defaults to 'asi_grupa_6_autogluon'.
        learning_rate (float): Learning rate used in the experiment. Defaults to 0.01.
        epochs (int): Number of epochs used in the experiment. Defaults to 10.
        log_additional_info (bool): Flag to log additional information to W&B. Defaults to False.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: DataFrame with calculated metrics and confusion matrix.
  """

    # Initialize WandB run
    run = wandb.init(project=project_name, config={"learning_rate": learning_rate, "epochs": epochs})

    try:
        # Calculating metrics
        accuracy = accuracy_score(predictions_test['HeartDisease'], predictions_test['Prediction'])
        precision = precision_score(predictions_test['HeartDisease'], predictions_test['Prediction'])
        recall = recall_score(predictions_test['HeartDisease'], predictions_test['Prediction'])
        f1 = f1_score(predictions_test['HeartDisease'], predictions_test['Prediction'])
        confusion_matrix = pd.crosstab(
            predictions_test['HeartDisease'],
            predictions_test['Prediction'],
            rownames=['Actual'],
            colnames=['Predicted']
        )

        # Log metrics
        wandb.log({"conf_mat": wandb.plot.confusion_matrix(probs=None, y_true=predictions_test['Potability'].values,
                                                           preds=predictions_test['Prediction'].values,
                                                           class_names=['0', '1']),
                   "accuracy": accuracy,
                   "precision": precision,
                   "recall": recall,
                   "f1_score": f1})

        return pd.DataFrame({
            'accuracy': [accuracy],
            'precision': [precision],
            'recall': [recall],
            'f1_score': [f1]
        }), confusion_matrix

    except KeyError as e:
        print(f"KeyError: {e}. Ensure 'HeartDisease' and 'Prediction' are in predictions_test.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        run.finish()
