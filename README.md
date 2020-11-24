# CROPTOOL

This project aims to take objects with white backgrounds and crop them into real backgrounds automatically (and YOLO annotate them)

generate_image.py takes an image with a white background and extracts the object within it, producing a transparent background .png image.
overlay_image.py then takes in the object without a background (output of generate_image.py) and overlays it onto a larger background image.

# Steps
1. Place white background images in ./images/white_images/ folder and background images in ./images/backgrounds
2. Run python generate_image.py. New object images should be in ./images/objects folder
3. Run python overlay_image.py. Recombined images should be in in ./images/recombined-images and YOLO annotated .txt files should be in ./images/labels