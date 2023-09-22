import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

def absolute_digit_sum(number):
    total = sum([int(digit) for digit in str(abs(number))])
    while total >= 10:
        total = sum([int(digit) for digit in str(total)])
    return total

def plot_dots(num_list):
    num_list = [absolute_digit_sum(number) for number in num_list]

    # Define a list of colors
    color_list = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'black', 'grey']

    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.axis('off')

    radius = 0.5  # radius of the dots
    diameter = 2 * radius

    count = 0
    row = 0
    color_index = 0  # start with the first color
    sum_so_far = num_list[color_index]  # sum up to the current color
    print(num_list)
    print(sum(num_list))
    while count < sum(num_list):
        for col in range(row + 1):
            if count == sum(num_list):
                break
            # Update the color if necessary
            while count >= sum_so_far:
                color_index += 1
                sum_so_far += num_list[color_index]

            color = color_list[(num_list[color_index] - 1) % len(color_list)] 
            x = col * diameter - row * radius
            y = -row * diameter * np.sqrt(3) / 2
            circle = Circle((x, y), radius, color=color)
            ax.add_patch(circle)
            count += 1
        row += 1

    ax.relim()
    ax.autoscale_view()

    plt.show()

# Example: plot 15 dots
plot_dots([2701])
