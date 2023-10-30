import pandas as pd
import csv
import os
import glob
import dload


# Define a function to replace '/' with '-'
def replace_slash_with_dash(column_name):
    return column_name.replace('/', '-')


# defining input csv file
url = ('https://api.open-meteo.com/v1/forecast?latitude=22.714183&longitude=120.337895&hourly=temperature_2m,'
       'relativehumidity_2m,dewpoint_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,'
       'snowfall,snow_depth,weathercode,pressure_msl,surface_pressure,cloudcover,cloudcover_low,cloudcover_mid,'
       'cloudcover_high,visibility,evapotranspiration,et0_fao_evapotranspiration,vapor_pressure_deficit,'
       'windspeed_10m,windspeed_80m,windspeed_120m,windspeed_180m,winddirection_10m,winddirection_80m,'
       'winddirection_120m,winddirection_180m,windgusts_10m,temperature_80m,temperature_120m,temperature_180m,'
       'uv_index,uv_index_clear_sky,is_day,cape,freezinglevel_height,shortwave_radiation,direct_radiation,'
       'diffuse_radiation,direct_normal_irradiance,terrestrial_radiation,shortwave_radiation_instant,'
       'direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,'
       'terrestrial_radiation_instant,temperature_1000hPa,relativehumidity_1000hPa,cloudcover_1000hPa,'
       'windspeed_1000hPa,winddirection_1000hPa,'
       'geopotential_height_1000hPa&daily=weathercode&timeformat=unixtime&timezone=auto&models=best_match&format=csv')
dload.save(url, "forecast.csv", True)
input_csv_file = 'forecast.csv'

# pre-processing csv open-meteo
with open(input_csv_file, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

first_two_rows = data[:2]

with open('location specs.csv', 'w', newline='') as new_file:
    writer = csv.writer(new_file)
    writer.writerows(first_two_rows)

del data[:3]

with open(input_csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# defining location data
location_specs = 'location specs.csv'

# specifying columns to concat and initiating dataframes
df = pd.read_csv(input_csv_file)
df2 = pd.read_csv(location_specs)
df3 = pd.DataFrame(data={'': [''], '_result': ['']})

# concat the two dataframes
frames = [df3, df2, df]
result = pd.concat(frames, axis=1)

# iterate through the columns and rename them
result = result.rename(columns=replace_slash_with_dash)

# fill NaN
result.ffill(inplace=True)

# define the directory where you want to save the CSV files
output_directory = 'openMeteoParameters'

# make sure the directory exists, or create it if it doesn't
os.makedirs(output_directory, exist_ok=True)

# loop through the columns and save the CSV files to the specified directory
for column in result.columns[9:]:
    selected_columns_df = result[
        ['', '_result', 'latitude', 'longitude', 'elevation', 'utc_offset_seconds', 'timezone',
         'timezone_abbreviation', 'time', 'is_day ()', column]]

    # construct the full path to the CSV file in the specified directory
    output_file_path = os.path.join(output_directory, f'{column}.csv')

    # save the DataFrame to the CSV file in the specified directory
    selected_columns_df.to_csv(output_file_path, index=False, sep=',')

files = glob.glob(output_directory + "/*.csv")
for csv in files:
    filename = os.path.basename(csv)[:-4]  # extract the file name without extension
    measurements = pd.read_csv(csv)
    # measurements.insert(2, column='_measurement', value=filename)
    # To-Do tambahin logic mana forecast mana present mana historical
    measurements.insert(2, column='_measurement', value='Forecast')
    measurements.rename(columns={'Unnamed: 0': ''}, inplace=True)
    output_file_path = os.path.join(output_directory, f'{filename}.csv')
    measurements.to_csv(output_file_path, index=False, sep=',')
