import pandas as pd
import random
from datetime import datetime, timedelta

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

data = []
for _ in range(100):  # Example: 100 data points
    time = random_date(datetime(2020, 1, 1), datetime(2022, 12, 31)).strftime("%Y-%m-%d %H:%M:%S")
    traffic = random.randint(0, 50)
    data.append([time, traffic])

df = pd.DataFrame(data, columns=['time', 'traffic'])
df.to_csv('/Users/jrdegbe/Desktop/Traffic-task-GCP/data//test_data.csv', index=False)
