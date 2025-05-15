# Visibility Based Pursuit Evasion in an Occupancy Grid

## Core Functionality (Current)

The functionality of the program currently is:

- Use a 2D binary NumPy array to represent an object environment with obstacles
- Calculate visibility from a given point within an obstacle environment
- Calculate visibility on a straight path of given direction and distance within an obstacle environment
- Track the state of non-visible regions along a path through an obstacle environment
- Visualize the state of an obstacle environment using PyCairo as a PNG or mp4

## How It Works
A "Grid" object is the base of the process. It is comprised of an occupancy grid that can represent an object environment with just the obstacles or and object environment with occupants

The simulated occupancy grid is represented as a binary 2D NumPy array using "1" to represent a zone that can not be seen through or moved through and a "0" to represent a zone that can be seen through and moved through.

Given a point within an obstacle environment supplied by the user, a [cone-based visibility algorithm](https://towardsdatascience.com/a-quick-and-clear-look-at-grid-based-visibility-bf63769fbc78/) is used to calculate the non-visible zones within the environment and then a Grid object is constructed with just the non-visible regions designated ---

PyCairo is used to visualize the state of a path within an obstacle environment at any given discrete step. The Grid object contains a method to visualize each index within the array as a square of any given color on a PyCairo canvas. Multiple Grid objects can be represented on one canvas, this occurs when Grid objects containing the non-visible regions for a given point and the grid object that represent the obstacles are combined to visualize an entire problem state. [Learn more about PyCairo.](https://pycairo.readthedocs.io/en/latest/index.html)

The overall flow of information is:
- 

## Core Files

### Grid.py

