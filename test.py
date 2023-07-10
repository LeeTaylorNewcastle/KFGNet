"""
Author: Lee Taylor

test.py : test.py - test the C3D model from: https://arxiv.org/pdf/2206.13318v3.pdf
"""
from model import C3D
from functions import dataloader_test
import torch.nn.functional as f
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


if __name__ == '__main__':
    # Init. lightweight C3D model
    c3d = C3D(num_classes=2)

    # print(f"\nc3d.train_c3d() = {c3d.train_c3d(1)}")
    c3d.load_checkpoint("checkpoints/C3D_at_epoch39.pth")

    preds = []
    labels_list = []

    # outputs, vtemp = self(inputs)  # prediction, temporal weights
    for i, data in enumerate(dataloader_test()):
        # model input-output
        inputs, labels = data
        outputs, vtemp = c3d(inputs)

        outputs_vals = f.softmax(outputs[0], dim=0).detach().numpy()
        outputs_vals_rounded = [round(outputs_vals[0]), round(outputs_vals[1])]
        print(f"outputs = {outputs_vals_rounded}, labels = {labels}")

        # Save predictions and labels for evaluation
        preds.append(outputs_vals_rounded[0])
        labels_list.append(int(labels[0]))

    print("Finished Predicting")
    print()

    # Inefficient naming
    y_pred = preds
    y_test_single_label = labels_list

    # Debug output
    print(f"y_test_single_label = {labels_list}")
    print(f"y_pred = {preds}")

    # Create a confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_test_single_label, y_pred).ravel()

    # Compute metrics
    accuracy = accuracy_score(y_test_single_label, y_pred)
    sensitivity = recall_score(y_test_single_label, y_pred)  # Sensitivity is the same as Recall
    specificity = tn / (tn+fp)
    precision = precision_score(y_test_single_label, y_pred)
    f1 = f1_score(y_test_single_label, y_pred)

    metrics = [accuracy, sensitivity, specificity, precision, f1]
    for i, v in enumerate(metrics):
        metrics[i] = str(round(v * 100, 2)) + "%"

    print(f"Accuracy: {metrics[0]}")
    print(f"Sensitivity: {metrics[1]}")
    print(f"Specificity: {metrics[2]}")
    print(f"Precision: {metrics[3]}")
    print(f"F1-score: {metrics[4]}")

    # Mark EOF
    pass