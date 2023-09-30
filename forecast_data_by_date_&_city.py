import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import datetime
import numpy as np

# Load your dataset (assuming it's in a CSV file)
data = pd.read_csv("unique_dates_cities_df.csv")

data = data.drop("Unnamed: 0", axis=1)

# Preprocessing
# Assuming your dataset has columns: 'datetime', 'city', 'count'
# Convert the 'datetime' column to a proper datetime format
data['datetime'] = pd.to_datetime(data['datetime'])

# Extract relevant features from the datetime column
data['year'] = data['datetime'].dt.year
data['month'] = data['datetime'].dt.month
data['day'] = data['datetime'].dt.day
data['day_of_week'] = data['datetime'].dt.dayofweek  # Monday = 0, Sunday = 6

# One-hot encode the 'city' column
data = pd.get_dummies(data, columns=['city'], prefix='city')

# Split the data
X = data.drop(["count", "datetime"], axis=1)  # Features
y = data["count"]  # Target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


def model_training():
    # Model Training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Model Evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print(f"Root Mean Squared Error: {rmse}")


def save_model():
    # Save the model to a file
    joblib.dump(model, 'linear_regression_model.pkl')

# model_training()
# save_model()


# Load the saved model from the file
model = joblib.load('models/linear_regression_model.pkl')


def predict_count_for_date_and_city(date, city):
    # Prepare input features for prediction
    input_data = {
        'year': [date.year],
        'month': [date.month],
        'day': [date.day],
        'day_of_week': [date.weekday()],
    }

    # Get the list of all city columns used during training
    city_columns = [col for col in X_train.columns if col.startswith('city_')]

    # Set all city columns to 0
    for col in city_columns:
        input_data[col] = [0]

    # Set the corresponding city column to 1 based on the input city
    input_data[f'city_{city}'] = [1]

    # Make predictions
    prediction = model.predict(pd.DataFrame(input_data))
    return prediction[0]


# Example usage:
date_to_predict = datetime.datetime(2020, 11, 15)  # Replace with the desired date
city_to_predict = "york"  # Replace with the desired city
predicted_count = predict_count_for_date_and_city(date_to_predict, city_to_predict)
print(f"Predicted count for {date_to_predict} in {city_to_predict}: {predicted_count}")
