# Import necessary libraries
import math
import random
import tkinter as tk
from tkinter import messagebox

# Initialize empty lists to store mobility data and device properties
array = []  # List to store mobility data
vel = []  # List to store velocities of devices
x = []  # List to store x-coordinates of devices
y = []  # List to store y-coordinates of devices

# Define the type of mobility: 'linear' or 'circular'
mobility_type = "Linear"  # Set mobility_type = "circular" for circular motion

# Total number of devices
n = 3

# List of device IDs (1-indexed) present in the file
deviceid = [1, 3, 5]

# Define steps in distance and time
# Steps in distance device has to move based on velocity
# Steps in distance =  velocity * distanceStep
distanceStep = 1

# Time gap between two locations/positions
# time(s) = lengthOfSteps / timeStep, formula to calculate the next position time
timeStep = 5.0

timePerStep = 3  # Time per step

# Define the range at which time will be added into mobility.txt file
lengthOfSteps = 1801

# Define the velocity at which devices are moving
velocity = 8.0

# Define the initial position of devices
x_coordinates = 280.0
y_coordinates = 400.0

# Define the boundaries of the grid
grid_min_x = 0.0
grid_min_y = 0.0
grid_max_x = 1000.0
grid_max_y = 1000.0

# Initialize velocities, x, and y coordinates for each device
for i in range(0, n):
    vel.append(velocity)
    x.append(x_coordinates)
    y.append(y_coordinates)


# Function to check if coordinates are within the grid
def condition(x, y):
    """
    Checks if a set of coordinates (x, y) falls within the defined grid boundaries.

    Args:
        x (float): x-coordinate
        y (float): y-coordinate

    Returns:
        int: 1 if coordinates are within the grid, 0 otherwise.
    """
    if x < grid_min_x or x > grid_max_x or y < grid_min_y or y > grid_max_y:
        return 0  # Invalid grid length value
    else:
        return 1


# Function for generating random coordinates for circular motion
def generaterandominteger_Circular(x, y, dperstep, angle,velocity):
    """
    Generates random coordinates for circular motion.

    Args:
        x (float): x-coordinate
        y (float): y-coordinate
        dperstep (float): distance per step
        angle (float): current angle

    Returns:
        float: New x-coordinate
        float: New y-coordinate
        float: New angle
    """
    new_angle = angle + velocity * distanceStep / dperstep
    a = x + dperstep * math.cos(new_angle)
    b = y + dperstep * math.sin(new_angle)
    if condition(a, b) == 1:
        return (a, b, new_angle)
    else:
        return (x, y, angle)
# Function for generating random coordinates for linear motion
def generaterandominteger_Linear(x, y, dperstep):
    """
    Generates random coordinates for linear motion.

    Args:
        x (float): x-coordinate
        y (float): y-coordinate
        dperstep (float): distance per step

    Returns:
        float: New x-coordinate
        float: New y-coordinate
    """
    a = x
    b = y + dperstep
    return a, b


# Generate mobility data for each device
for i in range(n):
    # To Calculate Max Distance a no can move based on velocity
    dperstep = vel[i] * distanceStep
    array.append("0.0, %d ,%.1f, %.1f ,0.0" % (deviceid[i], x[i], y[i]))
    # To calculate the Angle randomly based on are of circle for circular motion
    rint = random.randint(0, 360)
    angle = math.radians(rint)
    # Loop through the time steps
    for j in range(1, lengthOfSteps):
        # Check if it's time for the device to move
        if j % timePerStep == 0:
            # Calculate the time at which the device will move
            time = j / timeStep  # Time at which device will move.
            # Store current x and y coordinates
            x1 = x[i]
            y1 = y[i]
            angle1 = angle
            # Check for type of mobility: 'linear' or 'circular'
            if mobility_type == "Linear":
                x[i], y[i] = generaterandominteger_Linear(x1, y1, dperstep)
            else:
                x[i], y[i], angle = generaterandominteger_Circular(x1, y1, dperstep, angle1,velocity)

            # Condition to check whether the newly generated X and Y Coordinates are within the grid
            if condition(x[i], y[i]) == 0:
                break
            # Updating the array variable with the new set of values Time, Device ID, X-Coordinate and Y-Coordinate
            # and assuming that Z-Coordinate always 0.0
            array.append("%.1f, %d, %.1f ,%.1f, 0.0" % (time, deviceid[i], x[i], y[i]))

# Write data to a CSV file
fields = ["#Time(s), Device ID, X,Y,Z"]
filename = "mobility.csv"
with open(filename, 'w') as csvfile:
    csvfile.writelines(fields)
    for line in array:
        csvfile.writelines('\n' + line)

# Create a GUI window
root = tk.Tk()

# Hide the main window
root.withdraw()

# Get the full file path
import os
full_path = os.path.abspath(filename)

# Show a popup message with file path
messagebox.showinfo("File Generated", f"The file '{filename}' has been generated.\n\nLocation: {full_path}")

# Destroy the GUI window
root.destroy()