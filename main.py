import cv2
import os
import numpy as np

def create_binary_mask(image, mask_output_dir, index):
    # Extract the alpha channel from the image
    alpha_channel = image[:, :, 3]

    # Create a binary mask using the alpha channel
    binary_mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)[1]

    # Save the binary mask
    output_path = os.path.join(mask_output_dir, f"{index}_mask.png")
    cv2.imwrite(output_path, binary_mask)
    print(f"Binary mask saved at {output_path}")

def generate_random_background(shape):
    # Choose between solid color, striped, and blended color backgrounds
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



def add_random_background(image, bg_output_dir, index):
    # Generate a random background
    random_bg = generate_random_background(image.shape)

    # Combine the original image with the random background
    foreground = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    background = cv2.cvtColor(random_bg, cv2.COLOR_BGR2RGB)
    alpha = foreground[:, :, 3] / 255.0
    alpha_expanded = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)

    result = cv2.multiply(alpha_expanded, foreground[:, :, :3].astype(float)) + \
             cv2.multiply(1 - alpha_expanded, background.astype(float))
    result = result.astype(np.uint8)

    # Save the image with the random background
    output_path = os.path.join(bg_output_dir, f"{index}_with-bg.png")
    cv2.imwrite(output_path, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
    print(f"Image with random background saved at {output_path}")

def process_images(input_dir, mask_output_dir, bg_output_dir):
    # Create the output directories if they don't exist
    if not os.path.exists(mask_output_dir):
        os.makedirs(mask_output_dir)
    if not os.path.exists(bg_output_dir):
        os.makedirs(bg_output_dir)

    # Loop through all images in the input directory
    for index, filename in enumerate(os.listdir(input_dir), start=1):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_image_path = os.path.join(input_dir, filename)
            image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
            create_binary_mask(image, mask_output_dir, index)
            add_random_background(image, bg_output_dir, index)

if __name__ == "__main__":
    input_dir = "original-images"
    mask_output_dir = "modified-images/mask"
    bg_output_dir = "modified-images/with_bg"

    process_images(input_dir, mask_output_dir, bg_output_dir)
