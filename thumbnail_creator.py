import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
INPUT_DIR = r'E:\Images'
OUTPUT_DIR = r'F:\Thumbnails'
THUMBNAIL_SIZE = (128, 128)

def create_thumbnail(image_path, output_dir, size):
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            base_name = os.path.basename(image_path)
            thumbnail_path = os.path.join(output_dir, f'thumb_{base_name}')
            img.save(thumbnail_path)
            return thumbnail_path
    except Exception as e:
        print(f'Error processing {image_path}: {e}')
        return None

def rename_thumbnail(thumbnail_path):
    try:
        base_name = os.path.basename(thumbnail_path)
        new_name = f'renamed_{base_name}'
        new_path = os.path.join(os.path.dirname(thumbnail_path), new_name)
        os.rename(thumbnail_path, new_path)
        return new_path
    except Exception as e:
        print(f'Error renaming {thumbnail_path}: {e}')
        return None

def process_images(input_dir, output_dir, size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.gif', '.bmp'))]

    with ThreadPoolExecutor() as executor:
        resize_futures = {executor.submit(create_thumbnail, img, output_dir, size): img for img in image_files}

        thumbnails = []
        for future in as_completed(resize_futures):
            result = future.result()
            if result:
                thumbnails.append(result)

        rename_futures = {executor.submit(rename_thumbnail, thumb): thumb for thumb in thumbnails}    

        for future in as_completed(rename_futures):
            result = future.result()
            if result:
                print(f'Thumbnail created and renamed: {result}')

if __name__ == "__main__":
    process_images(INPUT_DIR, OUTPUT_DIR, THUMBNAIL_SIZE)



 



        

