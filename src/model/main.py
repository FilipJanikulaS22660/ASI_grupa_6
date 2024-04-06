# Import packages
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Load the CSV data from the GitHub link
url = 'https://raw.githubusercontent.com/FilipJanikulaS22660/ASI_grupa_6/main/data/prepared_final.csv'

data = pd.read_csv(url, sep=',')
print(data.columns)

# Check how many records are null
null_counts = pd.DataFrame(data[data.select_dtypes('number').columns].isna().sum(), columns=['Null Counts'])
null_counts

# Drop column 'Gaze Vector Right Z', because it contains only NaN values
data = data.drop('Gaze Vector Right Z', axis=1)

data.head()

# Drop all records, where any of the rows or columns is empty
data.dropna(how='any', inplace=True)

X = data.drop('Class', axis=1)  # Assuming 'Class' is the target column
y = data['Class']
data.info()

columns_to_be_converted_to_floats = ['RecordingTime [ms]', 'Participant', 'Index Right', 'Pupil Diameter Right [mm]', 'Point of Regard Right X [px]']
data[columns_to_be_converted_to_floats] = data[columns_to_be_converted_to_floats].astype(float)
data.info()

# Replace missing values with NaN
# data = data.replace('?', pd.NA)

# Separate features and target
X = data.drop('Class', axis=1)
y = data['Class']

# Encode categorical columns
categorical_cols = X.dtypes == object
categorical_cols = list(categorical_cols[categorical_cols].index)
label_encoder = LabelEncoder()

for col in categorical_cols:
    X[col] = label_encoder.fit_transform(X[col])

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Classifier model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model's performance
print("Precision:", accuracy_score(y_test, y_pred))
print("Classification report:\n", classification_report(y_test, y_pred))

# Analyze feature importance
importances = model.feature_importances_
feature_names = X.columns
feature_importances = pd.Series(importances, index=feature_names)
feature_importances.sort_values(ascending=False, inplace=True)
print("Feature Importances:\n", feature_importances)