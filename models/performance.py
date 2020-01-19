import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
from logging import warning


def get_performance_measures(model, x_test, y_test):
    # predict
    performance_measures = {}
    y_test_pred = model.predict(x_test)

    # accuracy
    accuracy = accuracy_score(y_test, y_test_pred)
    performance_measures['accuracy'] = accuracy

    # f1 score
    f1 = f1_score(y_test, y_test_pred)
    performance_measures['f1'] = f1

    # confusion matrix
    cm = confusion_matrix(y_test, y_test_pred)
    cm_df = pd.DataFrame(cm, columns=['actual_0', 'actual_1'],
                            index=['predicted_0', 'predicted_1'])
    performance_measures['confusion_matrix'] = cm_df

    try:
        y_test_pred_proba = model.predict_proba(x_test)
        # ROC-AUC score
        roc_auc = roc_auc_score(y_test, y_test_pred_proba[:,1])
        performance_measures['roc_auc'] = roc_auc
    except Exception as e:
        warning(e)

    return performance_measures
