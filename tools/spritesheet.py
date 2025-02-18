from PIL import Image
import os

def create_sprite_sheet(image_folder, output_file):
    # Get a list of image file paths in the folder
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    
    if not image_files:
        print("No images found in the specified folder.")
        return

    # Open all images and ensure they are the same size
    images = [Image.open(img) for img in image_files]
    width, height = images[0].size

    for img in images:
        if img.size != (width, height):
            print("All images must have the same dimensions.")
            return

    # Determine the dimensions of the sprite sheet
    num_images = len(images)
    sprite_width = width * num_images
    sprite_height = height

    # Create a new blank image for the sprite sheet
    sprite_sheet = Image.new("RGBA", (sprite_width, sprite_height))

    # Paste each image into the sprite sheet
    for index, img in enumerate(images):
        sprite_sheet.paste(img, (index * width, 0))

    # Save the sprite sheet
    sprite_sheet.save(output_file)
    print(f"Sprite sheet saved as {output_file}")

# Example usage
# Specify the folder containing images and the output sprite sheet file name
image_folder = "C:/godot_projects/plinko2/assets/plipanimation"
output_file = "C:/godot_projects/plinko2/anim1.png"
create_sprite_sheet(image_folder, output_file)
