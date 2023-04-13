import os
import shutil

def cleanup_modified_images(dirs_to_clean):
    for dir_to_clean in dirs_to_clean:
        if os.path.exists(dir_to_clean):
            for filename in os.listdir(dir_to_clean):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    os.remove(os.path.join(dir_to_clean, filename))
            print(f"Removed all images from {dir_to_clean}")
        else:
            print(f"{dir_to_clean} does not exist")

dirs_to_clean = ['modified_images/mask', 'modified_images/with_bg']
cleanup_modified_images(dirs_to_clean)

