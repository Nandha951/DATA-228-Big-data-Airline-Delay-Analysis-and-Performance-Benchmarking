import pandas as pd

# Load the datasets
import os
all_data = pd.DataFrame()
for filename in os.listdir("./Dataset"):
    if filename.startswith("2024_") and filename.endswith(".csv"):
        filepath = os.path.join("./Dataset", filename)
        data = pd.read_csv(filepath, dtype={'CarrierDelay': float, 'WeatherDelay': float, 'NASDelay': float, 'SecurityDelay': float, 'LateAircraftDelay': float, 'ArrDelay': float})
        all_data = pd.concat([all_data, data], ignore_index=True)

all_data["FlightDate"] = pd.to_datetime(all_data["FlightDate"])
all_data["DayOfWeek"] = all_data["FlightDate"].dt.day_name()

data = all_data

# Data Cleaning (Handling Missing Values)
data = data.dropna(subset=["CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"])

# Calculate the average delay for each type of delay
avg_delays = {
    "avg_carrier_delay": data["CarrierDelay"].mean(),
    "avg_weather_delay": data["WeatherDelay"].mean(),
    "avg_nas_delay": data["NASDelay"].mean(),
    "avg_security_delay": data["SecurityDelay"].mean(),
    "avg_late_aircraft_delay": data["LateAircraftDelay"].mean()
}

# Find the delay type with the highest average delay
most_common_delay = max(avg_delays, key=avg_delays.get)

# Print the insights
print("Average Delays:")
for delay_type, avg_delay in avg_delays.items():
    print(f"{delay_type}: {avg_delay:.2f}")

print(f"\nMost Common Delay Type: {most_common_delay}")

# Group by origin and calculate average delays
origin_delays = data.groupby("Origin")[["CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"]].mean()

# Sort by average carrier delay
origin_delays = origin_delays.sort_values(by="CarrierDelay", ascending=False)

# Find the busiest airport (based on number of departures)
busiest_airport = data["Origin"].value_counts().idxmax()
print(f"\nBusiest Airport: {busiest_airport}")

# Calculate the average arrival delay
avg_arrival_delay = data["ArrDelay"].mean()
print(f"\nAverage Arrival Delay: {avg_arrival_delay:.2f} minutes")

# Find the airport with the highest average arrival delay
airport_avg_arrival_delay = data.groupby("Origin")["ArrDelay"].mean()
highest_avg_arrival_delay_airport = airport_avg_arrival_delay.idxmax()
highest_avg_arrival_delay = airport_avg_arrival_delay.max()
print(f"\nAirport with Highest Average Arrival Delay: {highest_avg_arrival_delay_airport} ({highest_avg_arrival_delay:.2f} minutes)")

# Calculate the correlation between carrier delay and late aircraft delay
correlation = data["CarrierDelay"].corr(data["LateAircraftDelay"])
print(f"\nCorrelation between Carrier Delay and Late Aircraft Delay: {correlation:.2f}")

# Find the most common destination airport
most_common_destination = data["Dest"].value_counts().idxmax()
print(f"\nMost Common Destination Airport: {most_common_destination}")

# Analyze average delay per day of the week
average_delay_per_day = data.groupby("DayOfWeek")["ArrDelay"].mean().sort_values()
# Find the carrier with the highest average delay
carrier_avg_delay = data.groupby("Reporting_Airline")["ArrDelay"].mean()
highest_avg_delay_carrier = carrier_avg_delay.idxmax()
highest_avg_delay = carrier_avg_delay.max()
print(f"\nCarrier with Highest Average Delay: {highest_avg_delay_carrier} ({highest_avg_delay:.2f} minutes)")

# Analyze average taxi-out time
avg_taxi_out_time = data["TaxiOut"].mean()
print(f"\nAverage Taxi-Out Time: {avg_taxi_out_time:.2f} minutes")

# Calculate the percentage of flights delayed
total_flights = len(data)
delayed_flights = len(data[data["ArrDelay"] > 0])
percentage_delayed = (delayed_flights / total_flights) * 100
print(f"\nPercentage of Flights Delayed: {percentage_delayed:.2f}%")

# Analyze the average delay per month
data["Month"] = data["FlightDate"].dt.month
average_delay_per_month = data.groupby("Month")["ArrDelay"].mean()
print("\nAverage Delay per Month:")
print(average_delay_per_month)

# Analyze the average delay per carrier
average_delay_per_carrier = data.groupby("Reporting_Airline")["ArrDelay"].mean()
print("\nAverage Delay per Carrier:")
print(average_delay_per_carrier)

# Show top 10 origins with highest carrier delay
print("\nTop 10 Origins with Highest Carrier Delay:")
print(origin_delays.head(10))