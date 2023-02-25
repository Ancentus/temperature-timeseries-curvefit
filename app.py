import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from datetime import datetime

# Load the data from the CSV file into a numpy array
date, temperature = np.loadtxt('monthly_csv.csv', delimiter=',', skiprows=1,
                  usecols=(1, 2), unpack=True, 
                  dtype=[('date', object), ('temperature', float)],
                  converters={1: lambda d: datetime.strptime(d.decode(), '%Y-%m-%d')})

# Convert date strings to numerical values representing days since the first date
date_num = np.array([(d - date[0]).days for d in date])

# Define the function f(t) = a*cost(2*pi*t + b) + c
def f(t, a, b, c):
    return a * np.cos(t) * (2 * np.pi * t + b) + c

# Fit the function to the data using curve_fit
popt, pcov = curve_fit(f, date_num, temperature)

# Display the optimized parameters
print(popt)
print("a= ", popt[0], "+/-", pcov[0,0]**.5)
print("b= ", popt[1], "+/-", pcov[1,1]**.5)
print("c= ", popt[2], "+/-", pcov[2,2]**.5)


# Plot the data and the best fit model
plt.plot(date, temperature, 'b.', label='Data')
plt.plot(date, f(date_num, *popt), 'r-', label='Best fit model')

# Add axis labels and a legend
plt.xlabel('Date')
plt.ylabel(' Mean Temperature Anomaly (C)')
plt.legend()

# Display the plot
plt.show()
