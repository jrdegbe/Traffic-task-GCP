import pandas as pd
import logging
import os

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_csv_format(output_file):
    """
    Tests the transformed CSV file for correct format and data.

    :param output_file: Path to the generated CSV file.
    """
    if not os.path.exists(output_file):
        logging.error(f"File {output_file} does not exist.")
        return False

    try:
        # Read the CSV file
        data = pd.read_csv(output_file)

        # Test for 'time' column
        if 'time' not in data.columns:
            logging.error("'time' column is missing.")
            return False

        # Validate time format (example: '22-03-01 15:30')
        try:
            pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M')
        except ValueError:
            logging.error("Time column format is incorrect.")
            return False

        logging.info("CSV file format and time column are correct.")
        return True

    except Exception as e:
        logging.error(f"An error occurred while testing: {e}")
        return False

# File path to the generated CSV (update as necessary)
output_csv_file = '/Users/jrdegbe/Desktop/Traffic-task-GCP/data/traffic_data.csv'

# Run the test
test_result = test_csv_format(output_csv_file)

# Optional: Print the test result
print(f"Test Result: {'Passed' if test_result else 'Failed'}")
