from image_processing import process_images

if __name__ == "__main__":
    input_dir = "original_images_large"
    mask_output_dir = "modified_images/mask_large"
    bg_output_dir = "modified_images/with_bg_large"
    background_images_dir = "background_images"

    print("Processing images...")
    process_images(input_dir, mask_output_dir, bg_output_dir, background_images_dir)
    print("Done!")