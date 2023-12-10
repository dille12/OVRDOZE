import os
import cv2

def images_to_video(input_folder, output_file, fps=60):
    # Make sure the input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' not found.")
        return

    # List all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Sort the image files based on their names
    image_files.sort()

    # Get the first image to determine dimensions
    first_image = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, layers = first_image.shape

    # Initialize VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Write each frame to the video
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frame = cv2.imread(image_path)
        video.write(frame)

    # Release the VideoWriter
    video.release()
    print(f"Video created successfully: {output_file}")


folder_path = "C:/Users/Reset/Documents/GitHub/OVRDOZE/anim"

subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
print(subfolders)

for x in subfolders:
    input_folder = f"C:/Users/Reset/Documents/GitHub/OVRDOZE/anim/{x}"
    output_file = f"C:/Users/Reset/Documents/GitHub/OVRDOZE/anim_compressed/{x}/video.mp4"

    output_folder = f"C:/Users/Reset/Documents/GitHub/OVRDOZE/anim_compressed/{x}"

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    images_to_video(input_folder, output_file)
