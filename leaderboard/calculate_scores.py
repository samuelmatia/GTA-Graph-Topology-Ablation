from pathlib import Path
import pandas as pd
from sklearn.metrics import f1_score, accuracy_score

from leaderboard.hidden_labels_reader import read_hidden_labels


def calculate_scores(prediction_path: Path):
    """
    Calculate F1 and accuracy for a prediction file.
    """

    # Load predictions
    predictions = pd.read_csv(prediction_path)

    # Load hidden labels
    truth = read_hidden_labels()

    if truth is None:
        raise ValueError("Hidden labels could not be loaded")

    if len(predictions) != len(truth):
        raise ValueError("Prediction length does not match hidden labels")

    # Use last column as label (robust to header name differences)
    y_true = truth.iloc[:, -1]
    y_pred = predictions.iloc[:, -1]

    f1 = f1_score(y_true, y_pred, average="macro")
    acc = accuracy_score(y_true, y_pred)

    return {
        "validation_f1_score": f1,
        "validation_accuracy": acc
    }


def calculate_scores_pair(ideal_path: Path, perturbed_path: Path):
    """
    Calculate scores for both ideal and perturbed submissions
    and compute robustness gap.
    """

    scores_ideal = calculate_scores(ideal_path)
    scores_perturbed = calculate_scores(perturbed_path)

    robustness_gap = (
        scores_ideal["validation_f1_score"]
        - scores_perturbed["validation_f1_score"]
    )

    return {
        "validation_f1_ideal": scores_ideal["validation_f1_score"],
        "validation_f1_perturbed": scores_perturbed["validation_f1_score"],
        "robustness_gap": robustness_gap,
        "validation_accuracy_ideal": scores_ideal["validation_accuracy"],
        "validation_accuracy_perturbed": scores_perturbed["validation_accuracy"],
    }
