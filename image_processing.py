import cv2
import numpy as np
import os
from background_generators import generate_random_background, get_random_background_image

def create_binary_mask(image, mask_output_dir, index):
    """
    Creates a binary mask from the given image and saves it to the specified directory.

    :param image: input image in BGR format with an alpha channel
    :param mask_output_dir: output directory for the binary mask
    :param index: index of the image used for naming the output file
    """
    try:
        # Extract the alpha channel from the image
        alpha_channel = image[:, :, 3]

        # Create a binary mask using the alpha channel
        binary_mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)[1]

        # Save the binary mask
        output_path = os.path.join(mask_output_dir, f"{index}.png")
        cv2.imwrite(output_path, binary_mask)
    except IndexError:
        print(f"Skipping image {index} due to IndexError (missing alpha channel)")

def add_selected_background(image, bg_output_dir, index, background_images_dir, used_backgrounds):
    """
    Adds a randomly selected background image to the input image and saves the result.

    :param image: input image in BGR format with an alpha channel
    :param bg_output_dir: output directory for the image with the selected background
    :param index: index of the image used for naming the output file
    :param background_images_dir: directory containing background images
    :param used_backgrounds: set of used background image filenames to prevent repetition
    """
    try:
        # Get a random background image from the background_images_dir
        background_image = get_random_background_image(background_images_dir, used_backgrounds)

        # Combine the original image with the selected background
        foreground = image.copy()    
        background = cv2.resize(background_image, (image.shape[1], image.shape[0]))
        alpha = foreground[:, :, 3] / 255.0
        alpha_expanded = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)

        # Blend the foreground and background images using the alpha channel
        result = cv2.multiply(alpha_expanded, foreground[:, :, :3].astype(float)) + \
                cv2.multiply(1 - alpha_expanded, background.astype(float))
        result = result.astype(np.uint8)

        # Save the image with the selected background
        output_path = os.path.join(bg_output_dir, f"{index}_with_selected_bg.png")
        cv2.imwrite(output_path, result)
    except IndexError:
        print(f"Skipping image {index} due to IndexError (missing alpha channel)")


def add_random_background(image, bg_output_dir, index):
    """
    Generates a random background, adds it to the input image, and saves the result.

    :param image: input image in BGR format with an alpha channel
    :param bg_output_dir: output directory for the image with the random background
    :param index: index of the image used for naming the output file
    """
    try:
        # Generate a random background
        random_bg = generate_random_background(image.shape)

        # Combine the original image with the random background
        foreground = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        background = cv2.cvtColor(random_bg, cv2.COLOR_BGR2RGB)
        alpha = foreground[:, :, 3] / 255.0
        alpha_expanded = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)
        
        # Blend the foreground and background images using the alpha channel
        result = cv2.multiply(alpha_expanded, foreground[:, :, :3].astype(float)) + \
                cv2.multiply(1 - alpha_expanded, background.astype(float))
        result = result.astype(np.uint8)

        # Save the image with the random background
        output_path = os.path.join(bg_output_dir, f"{index}.jpg")
        cv2.imwrite(output_path, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
        # print(f"Image with random background saved at {output_path}")
    except IndexError:
        print(f"Skipping image {index} due to IndexError (missing alpha channel)")

def process_images(input_dir, mask_output_dir, bg_output_dir, background_images_dir):
    """
    Processes all images in the input directory, creates binary masks, adds random and selected backgrounds,
    and saves the results in the specified output directories.

    :param input_dir: directory containing input images
    :param mask_output_dir: output directory for binary masks
    :param bg_output_dir: output directory for images with added backgrounds
    :param background_images_dir: directory containing background images
    """
    # Create the output directories if they don't exist
    if not os.path.exists(mask_output_dir):
        os.makedirs(mask_output_dir)
    if not os.path.exists(bg_output_dir):
        os.makedirs(bg_output_dir)

    used_backgrounds = set()
    # Loop through all images in the input directory
    for index, filename in enumerate(os.listdir(input_dir), start=1):
        if index % 100 == 0:
            print(f"Processed {index} images")
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_image_path = os.path.join(input_dir, filename)
            image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
            create_binary_mask(image, mask_output_dir, index)
            add_random_background(image, bg_output_dir, index)
            # add_selected_background(image, bg_output_dir, index, background_images_dir, used_backgrounds)
