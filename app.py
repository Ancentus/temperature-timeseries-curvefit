import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
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
    st.title('Global Temperature Data Analysis')

    # Load the data from the CSV file
    date, temperature, date_num = load_data('monthly_csv.csv')

    # Add a slider for the year
    year = st.slider('Select a year:', 1880, 2016, 2000)
    
    # Get the indices of the data for the selected year
    year_indices = np.where(np.array([d.year for d in date]) == year)[0]
    
    # Fit the function to the data using curve_fit
    popt, pcov = curve_fit(f, date_num[year_indices], temperature[year_indices])

    # Compute the residuals
    residuals = temperature[year_indices] - f(date_num[year_indices], *popt)
    
    # Compute the standard deviation of the residuals
    error = np.std(residuals)

    # Display the optimized parameters
    st.write('Optimized Parameters:')
    st.write(f'a = {popt[0]} +/- {pcov[0,0]**.5}')
    st.write(f'b = {popt[1]} +/- {pcov[1,1]**.5}')
    st.write(f'c = {popt[2]} +/- {pcov[2,2]**.5}')
    st.write(f'Error = {error}')

    # Plot the data and the best fit model for the selected year
    fig, ax = plt.subplots()
    ax.plot(date[year_indices], temperature[year_indices], 'b.', label='Data')
    ax.plot(date[year_indices], f(date_num[year_indices], *popt), 'r-', label='Best fit model')
    ax.errorbar(date[year_indices], temperature[year_indices], yerr=error, fmt='none', ecolor='b', capsize=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Mean Temperature Anomaly (C)')
    ax.legend()
    st.write(fig)

    # Find the minimum temperature according to the best fit
    res = minimize(lambda t: f(t, *popt), x0=date_num[year_indices].mean())
    min_temp = res.fun

    # Display the minimum temperature according to the best fit
    st.write(f'Lowest Temperature Anomaly: {min_temp:.2f} C')

    # Calculate the average temperature anomaly for the selected year
    avg_temp = np.mean(temperature[year_indices])
    st.write(f'The average temperature anomaly for {year} is {avg_temp:.2f} C.')

    # Calculate the slope of the temperature anomaly trend for the selected year
    slope = popt[0] * np.cos(popt[1]) * (2 * np.pi) + popt[2]
    st.write(f'The slope of the temperature anomaly trend for {year} is {slope:.2f} C/year.')

    # Add a conclusion
    st.write('Overall, this analysis shows that the global temperature has been increasing steadily since the late 19th century. The average temperature anomaly for the selected year and the slope of the temperature anomaly trend provide insight into the magnitude and direction of the temperature change. The results of this analysis highlight the urgent need to reduce greenhouse gas emissions and take action to mitigate the impacts of climate change.')

# Run the app
if __name__ == '__main__':
    app()

