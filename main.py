from image_processing import process_images

if __name__ == "__main__":
    input_dir = "original_images"
    mask_output_dir = "modified_images/mask"
    bg_output_dir = "modified_images/with_bg"
    background_images_dir = "background_images"

    print("Processing images...")
    process_images(input_dir, mask_output_dir, bg_output_dir, background_images_dir)
    print("Done!")