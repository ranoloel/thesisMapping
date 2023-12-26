import os
from PIL import Image

def resize_images(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):  # Add other file types if needed
            img = Image.open(os.path.join(input_directory, filename))
            img.thumbnail((640, 640))
            img.save(os.path.join(output_directory, filename))

input_directory = 'D:/YOLOV7ModelComparison/test-image-to-640'
output_directory = 'D:/ForElmo/thesisMapping/FromColabElmoThesis/yolov7/inference/images'
resize_images(input_directory, output_directory)
print("Successfully Converted")
