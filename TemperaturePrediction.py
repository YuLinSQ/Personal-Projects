import sys
import os
import re  # Import the regular expression module
import pandas as pd
import numpy as np

#P(y=Sunny | time=600, weather_description=Cloudy) = P(y=Sunny)P(time=600|y=Sunny)P(weather_description=Cloudy|y=Sunny)
#add in clouds? decrease
#added in humidity, increase
#adding in both = decrease

def main(training_file, tests_folder):
    # Read training data from Excel file
    training_data = pd.read_excel(training_file)
    # Access a data point (for example, the first value)
    # try:
    #     first_value = training_data.iloc[0, 5]  # Assuming the first value is in the first row and first column
    #     print("First value in training data:", first_value)
    # except Exception as e:
    #     print(f"Error accessing data from training data: {e}")

    # Define a function to extract the numeric part of the filename
    def extract_numeric_part(filename):
        match = re.search(r'\d+', filename)  # Extract numeric part using regular expression
        return int(match.group()) if match else float('inf')  # Convert to integer if found, else use infinity

    # if training_data.iloc[0, 0] == 0:
    #     print("true")
    # else:
    #     print("false")
    weathers = ["Sunny", "Cloudy", "Partly cloudy", "Clear", "Overcast", "Patchy rain possible", "Moderate or heavy rain shower", "Moderate rain at times", "Heavy rain at times", "Light freezing rain", "Patchy moderate snow", "Moderate or heavy rain showers"]
    time = np.zeros((12, 4))
    w = np.zeros((12, 12))
    #clouds = ["Clear", "Partly cloudy", "Mostly clear", "Mostly cloudy", "Overcast"]
    #c = np.zeros((12, 5))
    humidity = ["High humidity", "Moderate humidity", "Low humidity"]
    h = np.zeros((12, 3))
    train = [0] * 12 # P(y=Sunny)
    for i in range(1, 7301):
    #for i in range(1, 11):
        for j in range(0, 12):
            if training_data.iloc[i, 5] == weathers[j]: # P(y=Sunny)
                train[j] = train[j]+1
                if training_data.iloc[i-1, 0] == 0:
                    time[j][0] = time[j][0]+1
                elif training_data.iloc[i-1, 0] == 600:
                    time[j][1] = time[j][1]+1
                elif training_data.iloc[i-1, 0] == 1200:
                    time[j][2] = time[j][2]+1
                elif training_data.iloc[i-1, 0] == 1800:
                    time[j][3] = time[j][3]+1
                for k in range(0, 12):
                    if training_data.iloc[i-1, 5] == weathers[k]:
                        w[j][k] = w[j][k]+1
                # for k in range(0, 5):
                #     if training_data.iloc[i-1, 10] == clouds[k]:
                #         c[j][k] = c[j][k]+1
                for k in range(0, 3):
                    if training_data.iloc[i-1, 7] == humidity[k]:
                        h[j][k] = h[j][k]+1
    #print(train)
    #print(time[0][0], time[0][1], time[0][2], time[0][3], time[1][1])
    #print(w[0][0], w[0][1], w[0][2])
    # Traverse through all subfolders recursively and read Excel files in sequential order
    for root, dirs, files in os.walk(tests_folder):
        files = sorted(files, key=extract_numeric_part)  # Sort files based on numeric part of the filename
        for filename in files:
            if filename.endswith('.xlsx'):
                # Found an Excel file, read it and access the first value
                excel_file_path = os.path.join(root, filename)
                tests_data = pd.read_excel(excel_file_path)
                weather_value_tests = tests_data.iloc[27, 5]
                time_value_tests = tests_data.iloc[27, 0]
                #cloud_value_tests = tests_data.iloc[27, 10]
                h_value_tests = tests_data.iloc[27, 7]
                ans = [0] * 12 # P(y=Sunny)
                time_train = [0] * 12 # P(time=600|y=Sunny)
                weather_train = [0] * 12 # P(weather_description=Cloudy|y=Sunny)
                #cloud_train = [0] * 12
                h_train = [0] * 12
                # for i in range(1, 1001):
                #     for j in range(0, 12):
                #         if training_data.iloc[i, 5] == weathers[j]: # P(y=Sunny)
                #             if training_data.iloc[i, 0] == time_value_tests:
                #                 time_train[j] = time_train[j]+1
                #             if training_data.iloc[i+1, 5] == weather_value_tests:
                #                 weather_train[j] = weather_train[j]+1
                for j in range(0, 12):
                    if(train[j]!=0):
                        if time_value_tests == 0:
                            time_train[j] = time[j][0]/train[j]
                        elif time_value_tests == 600:
                            time_train[j] = time[j][1]/train[j]
                        elif time_value_tests == 1200:
                            time_train[j] = time[j][2]/train[j]
                        elif time_value_tests == 1800:
                            time_train[j] = time[j][3]/train[j]
                        for k in range(0, 12):
                            if weather_value_tests == weathers[k]:
                                weather_train[j] = w[j][k]/train[j]
                        # for k in range(0, 5):
                        #     if cloud_value_tests == clouds[k]:
                        #         cloud_train[j] = c[j][k]/train[j]
                        for k in range(0, 3):
                            if h_value_tests == humidity[k]:
                                h_train[j] = h[j][k]/train[j]
                        #ans[j] = train[j]/7300*time_train[j]*weather_train[j] #P(y=Sunny | time=600, weather_description=Cloudy) = P(y=Sunny)P(time=600|y=Sunny)P(weather_description=Cloudy|y=Sunny)
                        #ans[j] = train[j]/7300*time_train[j]*weather_train[j]*cloud_train[j]
                        ans[j] = train[j]/7300*time_train[j]*weather_train[j]*h_train[j]
                        #ans[j] = train[j]/7300*time_train[j]*weather_train[j]*cloud_train[j]*h_train[j]
                        #ans[j] = train[j]/10*time_train[j]*weather_train[j]
                        #print(train[j], time_train[j], weather_train[j], "!")
                #compare clear, sunny, partly cloudy, and cloudy
                max = 0
                index = 0
                for j in range(0, 12):
                    if ans[j]>max:
                        max = ans[j]
                        index = j
                #print(max)
                print(weathers[index])
                #print(f"First value in Excel file {filename}:", first_value_tests)

if __name__ == "__main__":
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        #print("Usage: python3 NaiveBayesClassifier.py <training_file> <tests_folder>")
        sys.exit(1)
    
    # Get command-line arguments
    training_file = sys.argv[1]
    tests_folder = sys.argv[2]

    # Call the main function with the provided file names
    main(training_file, tests_folder)
