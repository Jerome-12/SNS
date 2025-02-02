"""

Automatically generated by Colab.

"""

#import libraries
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report

df1=pd.read_csv('/content/train.csv')

df2=pd.read_csv('/content/test.csv')

df1.head(5)

df2.head(5)

df1.info()

df2.info()

df1.shape

df2.shape

df1.describe()

df1.isna().sum()

df1.duplicated().any()

df1['price_range'].value_counts()

corr = df1.corr()

np.fill_diagonal(corr.values, 0)

corr.replace(0, np.nan, inplace=True)

plt.show()

corr

plt.figure(figsize=(20,10))
sns.heatmap(corr, annot=True, cmap='Reds')

corr.unstack().sort_values(kind='quicksort', na_position='first').drop_duplicates(keep='last')

corr.abs()['price_range'].sort_values(ascending=False)

sns.displot(df1, x='battery_power')

sns.displot(df1, x='clock_speed')

sns.displot(df1, x='ram')

sns.displot(df1, x='int_memory')

sns.lmplot(x='ram', y='price_range', data=df1, line_kws={'color': 'yellow'})
plt.yticks([0, 1, 2, 3])    # (0 - low cost, 1 - medium cost, 2 - high cost, 3 - very high cost)
plt.xlabel('Ram')
plt.ylabel('Price Range')
plt.show()

sns.boxenplot(x='price_range', y='battery_power', data=df1)
plt.xlabel('Price Range')
plt.ylabel('Battery Power')
plt.title('Battery Power\'s correlation to Price Range', weight='bold')
plt.show()

three_g = df1['three_g'].value_counts()
plt.title('Percentage of Mobiles with 3G', weight='bold')
labels_3g = ['3G', 'No 3G']
three_g.plot.pie(autopct="%.1f%%", labels=labels_3g)
plt.show()

four_g = df1['four_g'].value_counts()
plt.title('Percentage of Mobiles with 4G', weight='bold')
labels_4g = ['4G', 'No 4G']
four_g.plot.pie(autopct="%.1f%%", labels=labels_4g)
plt.show()

n_cores = df1['n_cores'].value_counts()
plt.title('Number of cores in mobile phones\n\n', weight='bold')
n_cores.plot.pie(autopct="%.1f%%", radius=1.5)
plt.show()

fig = px.scatter_3d(df1, x='ram', y='battery_power', z='px_width', color='price_range')
fig.show()

"""#Machine learning"""

X = df1.drop('price_range', axis=1)
y = df1['price_range']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.20, random_state=100)

models = {'KNN': KNeighborsClassifier(),
         'Linear Regression': LinearRegression(),
         'Random Forest': RandomForestClassifier()}

def fit_and_score(models, X_train, X_test, y_train, y_test):
    np.random.seed(42)

    model_scores = {}

    for name, model in models.items():
        model.fit(X_train, y_train)

        model_scores[name] = model.score(X_test, y_test)
    return model_scores

model_scores = fit_and_score(models=models,
                             X_train=X_train,
                            X_test=X_test,
                            y_train=y_train,
                            y_test=y_test)
model_scores

model_comp = pd.DataFrame(model_scores, index=['accuracy'])
model_comp.T.plot.bar()

train_scores = []

test_scores = []

neighbors = range(1, 21)

knn = KNeighborsClassifier()

for i in neighbors:
    knn.set_params(n_neighbors = i)

    knn.fit(X_train, y_train)

    train_scores.append(knn.score(X_train, y_train))

    test_scores.append(knn.score(X_test, y_test))

plt.plot(neighbors, train_scores, label="Train Scores")
plt.plot(neighbors, test_scores, label="Test Scores")
plt.xticks(np.arange(1, 21, 1))
plt.xlabel("Number of neighbors")
plt.ylabel("Model score")
plt.legend()

print(f"Maximum KNN score on the test data: {max(test_scores)*100:.2f}%")

knn = KNeighborsClassifier(n_neighbors=13)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print(f'KNN Model Score: {knn.score(X_test, y_test) * 100}%')

# Random Forest hyperparemeters

rf_grid = {"n_estimators": np.arange(10, 1000, 50),
           "max_depth": [None, 3, 5, 10],
           "min_samples_split": np.arange(2, 20, 2),
           "min_samples_leaf": np.arange(1, 20, 2)}

rs_rf = RandomizedSearchCV(RandomForestClassifier(),
                           param_distributions=rf_grid,
                           cv=5,
                           n_iter=20,
                           verbose=True)

rs_rf.fit(X_train, y_train);

rs_rf.best_params_

rs_rf.score(X_test, y_test)

rf_grid = {"n_estimators": np.arange(10, 1000, 50),
           "max_depth": [None, 3, 5, 10],
           "min_samples_split": np.arange(2, 20, 2),
           "min_samples_leaf": np.arange(1, 20, 2)}

gs_rf = RandomizedSearchCV(RandomForestClassifier(),
                           param_distributions=rf_grid,
                           cv=5,
                           n_iter=20,
                           verbose=True)

gs_rf.fit(X_train, y_train);

gs_rf.best_params_

gs_rf.score(X_test, y_test)

xgb = XGBClassifier(eval_metric='logloss', use_label_encoder=False)

xgb.fit(X_train, y_train)
xgb_pred = xgb.predict(X_test)
xgb.score(X_test, y_test)

params_xgb = {'n_estimators': [50,100,250,400,600,800,1000],
    'learning_rate': [0.2,0.5,0.8,1]}

rs_xgb =  RandomizedSearchCV(xgb, param_distributions=params_xgb, cv=5)
rs_xgb.fit(X_train, y_train)
xgb_pred_2 = rs_xgb.predict(X_test)
rs_xgb.score(X_test, y_test)

print(confusion_matrix(y_test, y_pred))

sns.set(font_scale=1) # Increase font size

def plot_conf_mat(y_test, y_preds):

    fig, ax = plt.subplots(figsize=(3, 3))
    ax = sns.heatmap(confusion_matrix(y_test, y_preds),
                     annot=True, # Annotate the boxes
                     cbar=False,
                    fmt='g', # no scientific notation
                    cmap='Blues')

    plt.xlabel("true label", weight='bold')
    plt.ylabel("predicted label", weight='bold')

plot_conf_mat(y_test, y_pred)

print(classification_report(y_test, y_pred))

print(f'Cross Validation Scores: ' + str(cross_val_score(knn, X, y, cv=5)))

print(f'Cross Validation Score (Mean): ' + str(np.mean(cross_val_score(knn, X, y, cv=5))))

