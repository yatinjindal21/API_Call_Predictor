import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set parameters for data generation
num_apis = 9  # Number of API types
start_date = datetime(2022, 1, 1)  # Start date
end_date = datetime(2025, 1, 1)    # End date (3 years duration)
api_codes = [f"A{i+1}" for i in range(num_apis)]  # API codes (A1, A2, ..., A9)

# Probability distribution to simulate high daytime activity
hour_probabilities = [0.02 if i < 8 or i >= 20 else 0.05 for i in range(24)]
hour_probabilities[8:20] = [0.07] * 12

# Normalize probabilities to ensure they sum to 1
hour_probabilities = np.array(hour_probabilities) / sum(hour_probabilities)

# Generate synthetic data
synthetic_data = []
current_date = start_date

while current_date < end_date:
    day_of_week = current_date.weekday()
    month_day = current_date.day
    special_occasion = (current_date.month == 12 and current_date.day == 25)  # Example: Christmas
    
    for api_code in api_codes:
        # Set base call volume: more on weekdays, less on weekends, with monthly variations
        base_calls = np.random.randint(1500, 2000) if day_of_week < 5 else np.random.randint(1000, 1500)
        if special_occasion:
            base_calls += np.random.randint(200, 400)
        elif month_day == 1 or month_day > 27:
            base_calls += np.random.randint(100, 200)

        # Generate calls for the day
        for _ in range(base_calls):
            hour = np.random.choice(range(24), p=hour_probabilities)
            minute = np.random.randint(0, 60)
            second = np.random.randint(0, 60)
            call_time = current_date.replace(hour=hour, minute=minute, second=second)
            
            # Introduce occasional outliers
            if np.random.rand() < 0.005:
                outlier_time = call_time + timedelta(minutes=np.random.randint(-60, 60))
                synthetic_data.append([api_code, outlier_time.strftime("%d-%m-%Y %H:%M")])

            # Normal data entry
            synthetic_data.append([api_code, call_time.strftime("%d-%m-%Y %H:%M")])

    current_date += timedelta(days=1)

# Convert to DataFrame and save to CSV
synthetic_df = pd.DataFrame(synthetic_data, columns=["API Code", "Time of Call"])
synthetic_df.to_csv("API_Call_Dataset.csv", index=False)
print("Synthetic dataset generated and saved as 'API_Call_Dataset.csv'")
