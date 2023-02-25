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

