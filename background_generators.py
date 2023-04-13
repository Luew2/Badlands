import cv2
import os
import random
import numpy as np

def get_random_background_image(background_images_dir, used_backgrounds, original_backgrounds=None):
    """
    Selects a random background image from the given background_images_dir, while ensuring that it has not been used before.
    
    :param background_images_dir: Directory containing background images.
    :type background_images_dir: str
    :param used_backgrounds: Set of filenames of the used background images.
    :type used_backgrounds: set
    :param original_backgrounds: List of the original background images.
    :type original_backgrounds: list
    :return: A random background image from the directory.
    :rtype: numpy.ndarray
    """
    if original_backgrounds is None:
        original_backgrounds = os.listdir(background_images_dir)
    available_images = list(set(original_backgrounds) - used_backgrounds)
    if not available_images:
        used_backgrounds.clear()
        available_images = original_backgrounds
    
    chosen_image = random.choice(available_images)
    used_backgrounds.add(chosen_image)
    
    return cv2.imread(os.path.join(background_images_dir, chosen_image), cv2.IMREAD_COLOR)


def generate_random_background(shape):
    """
    Generates a random background image by choosing between solid color, striped, and blended color backgrounds.
    
    :param shape: A tuple of the form (height, width, channels) representing the desired shape of the output background image.
    :type shape: tuple
    :return: A randomly generated background image with the specified shape.
    :rtype: numpy.ndarray
    """
    choice = np.random.choice(["solid", "striped", "blended"])

    if choice == "solid":
        # Create a random solid color background
        bg_color = np.random.randint(0, 256, size=3, dtype=np.uint8)
        bg = np.full((shape[0], shape[1], 3), bg_color, dtype=np.uint8)

    elif choice == "striped":
        # Create a striped background with random colors and directions
        num_slices = np.random.randint(2, 6)  # Choose the number of color slices (2 to 5)
        slice_width = shape[1] // num_slices
        slices = []

        for i in range(num_slices):
            color = np.random.randint(0, 256, size=3, dtype=np.uint8)
            single_slice = np.full((shape[0], slice_width, 3), color, dtype=np.uint8)
            slices.append(single_slice)

        # Concatenate the color slices to form the striped background
        bg = np.hstack(slices)

        # If the width of the concatenated slices is smaller than the original image width,
        # extend the last slice to match the width
        if bg.shape[1] < shape[1]:
            last_slice = np.full((shape[0], shape[1] - bg.shape[1], 3), slices[-1][0, 0], dtype=np.uint8)
            bg = np.hstack((bg, last_slice))

        # Rotate the stripes randomly between 0, 45, 90, and 135 degrees
        rotation_angle = np.random.choice([0, 45, 90, 135])
        rotation_matrix = cv2.getRotationMatrix2D((shape[1] // 2, shape[0] // 2), rotation_angle, 1)
        bg = cv2.warpAffine(bg, rotation_matrix, (shape[1], shape[0]))

    elif choice == "blended":
        # Create a random color background
        bg_color = np.random.randint(0, 256, size=(shape[0], shape[1], 3), dtype=np.uint8)

        # Apply a Gaussian blur to the background to create a blend of colors
        bg = cv2.GaussianBlur(bg_color, (25, 25), 10)

    return bg
