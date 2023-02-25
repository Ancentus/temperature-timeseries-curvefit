import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from datetime import datetime
import streamlit as st

# Define a function to load the data from the CSV file
def load_data(filename):
    date, temperature = np.loadtxt(filename, delimiter=',', skiprows=1,
                  usecols=(1, 2), unpack=True, 
                  dtype=[('date', object), ('temperature', float)],
                  converters={1: lambda d: datetime.strptime(d.decode(), '%Y-%m-%d')})
    date_num = np.array([(d - date[0]).days for d in date])
    return date, temperature, date_num

# Define the function f(t) = a*cost(2*pi*t + b) + c
def f(t, a, b, c):
    return a * np.cos(t) * (2 * np.pi * t + b) + c

# Define the Streamlit app
def app():
    # Set the title of the app
    st.title('Temperature Data Analysis')

    # Load the data from the CSV file
    date, temperature, date_num = load_data('monthly_csv.csv')

    # Fit the function to the data using curve_fit
    popt, pcov = curve_fit(f, date_num, temperature)

    # Display the optimized parameters
    st.write('Optimized Parameters:')
    st.write(f'a = {popt[0]} +/- {pcov[0,0]**.5}')
    st.write(f'b = {popt[1]} +/- {pcov[1,1]**.5}')
    st.write(f'c = {popt[2]} +/- {pcov[2,2]**.5}')

    # Plot the data and the best fit model
    fig, ax = plt.subplots()
    ax.plot(date, temperature, 'b.', label='Data')
    ax.plot(date, f(date_num, *popt), 'r-', label='Best fit model')
    ax.set_xlabel('Date')
    ax.set_ylabel('Mean Temperature Anomaly (C)')
    ax.legend()
    st.write(fig)

# Run the app
if __name__ == '__main__':
    app()

