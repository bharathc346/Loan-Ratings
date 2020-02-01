import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from bevel.bevel.linear_ordinal_regression import OrderedLogit
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=None, normalize=False):
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()

def accuracy(a,b):
    return sum(1 for x,y in zip(a,b) if x == y) / len(a)

df = pd.read_csv('/Users/bharathc/Desktop/Projects/Econometrics/final_regression_data.csv')
X = df
y = df.pop('TIER')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

ol = OrderedLogit()
ol.fit(X_train, y_train)
ol.print_summary()
y_pred = ol.predict_class(X_test)
print('Accuracy of ordinal regression classifier on test set: {:.2f}'.format(accuracy(y_pred, y_test)))
cm = confusion_matrix(y_test, y_pred)
plot_confusion_matrix(cm, ['Tier 1','Tier 2','Tier 3', 'Tier 4', 'Tier 5'])
