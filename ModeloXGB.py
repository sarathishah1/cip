import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
import xgboost as xgb
from sklearn.metrics import mean_squared_error

# Load your dataset
data = pd.read_csv("Life_Expectancy_Data_Europe_Recodificado.csv")

# Preprocessing
# Calculate column-wise means for numeric columns
numeric_means = data.select_dtypes(include='number').mean()

# Fill missing values with respective column means
data.fillna(numeric_means, inplace=True)

# Convert Population column to numeric
data['Population'] = pd.to_numeric(data['Population'], errors='coerce')

# Encode Country column using one-hot encoding
data = pd.get_dummies(data, columns=['Country'], drop_first=True)

# Fill missing values in Population column with its mean
data['Population'].fillna(data['Population'].mean(), inplace=True)

# Now, proceed with the remaining steps of preprocessing and modeling as before

# Encode categorical variables if any
# For example, using one-hot encoding
# data = pd.get_dummies(data)

# Split data into features and target variable
X = data.drop(columns=["Life_expectancy"])
y = data["Life_expectancy"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)


skf = StratifiedKFold(n_splits=5, random_state=44, shuffle=True)
for i, (train_index, test_index) in enumerate(skf.split(X, y)):
    print(f"Fold {i}: \nTrain index: {train_index}\nTest index: {test_index}")


# Model training
model = xgb.XGBRegressor(random_state=44)
model.fit(X_train, y_train)

# Model evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
r2score = model.score(X_test, y_test)
print("r2score:", r2score)



# Assuming you have already trained your XGBoost model and stored it in the variable 'model'



# Make predictions on new data
user_data = pd.read_csv("webdata.csv").drop("Life_expectancy", axis=1)  # Load your new data
#user_data = pd.read_csv("Life_Expectancy_Data_Europe_Recodificado.csv").drop("Life_expectancy", axis=1)
# Perform the same preprocessing steps as done for the training data (e.g., handle missing values, encode categorical variables)
# Assuming 'new_data' has been preprocessed similarly as 'data'
"""
We run the same preprocessing as the original data
"""


#numeric_means = user_data.select_dtypes(include='number').mean()
numeric_means = user_data.select_dtypes(include='number').mean()

# Fill missing values with respective column means
user_data.fillna(numeric_means, inplace=True)

# Convert Population column to numeric
user_data['Population'] = pd.to_numeric(user_data['Population'], errors='coerce')

# Encode Country column using one-hot encoding
user_data = pd.get_dummies(user_data, columns=['Country'], drop_first=True)

# Fill missing values in Population column with its mean
user_data['Population'].fillna(user_data['Population'].mean(), inplace=True)


"""
Now we can head over to the actual predicting
"""
# Make predictions using the trained model
predictions = model.predict(user_data)

# Print or use the predictions as needed
print(predictions)

print(model.feature_importances_)
print(model.get_booster().feature_names)
