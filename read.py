import cv2
import numpy as np
import math
import os
from PIL import Image

import cv2
import numpy as np
import os

def replace_and_save_contiguous(image_path, desired_color, desired_point, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    desired_color = np.array(desired_color)
    white_color = np.array([255, 255, 255])

    mask = cv2.inRange(image, desired_color, desired_color)
    image[mask == 0] = white_color

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        max_h = 40

        if h < max_h and w < 40:
            bounding_boxes.append((x, y, x+w, y+h))

    sorted_boxes = sort_bounding_boxes_by_distance(bounding_boxes, desired_point)[:15]
    extracts = []

    for i, box in enumerate(sorted_boxes):
        x1, y1, x2, y2 = box
        cropped_extracted_image = image[y1:y2, x1:x2]
        extracts.append(cropped_extracted_image)

        # Save the cropped region
        output_path = os.path.join(output_folder, f'crop_{i}.png')
        cv2.imwrite(output_path, cropped_extracted_image)

    return extracts

def distance_from_point(x, y, point):
    return math.sqrt((point[0] - x) ** 2 + (point[1] - y) ** 2)

def sort_bounding_boxes_by_distance(bounding_boxes, point):
    centers = [(box[0] + (box[2] - box[0]) / 2, box[1] + (box[3] - box[1]) / 2) for box in bounding_boxes]
    distances = [distance_from_point(x, y, point) for (x, y) in centers]
    boxes_with_distances = list(zip(bounding_boxes, distances))
    sorted_boxes_with_distances = sorted(boxes_with_distances, key=lambda x: x[1])
    sorted_bounding_boxes = [box for box, _ in sorted_boxes_with_distances]
    return sorted_bounding_boxes

def find_most_overlapping_image(directory_path, extracts):
    # Load the given image

    nums = []
    for given_image in extracts:

        max_overlap = 0
        most_similar_image_path = None

        # Iterate through each file in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # Load the current image
            current_image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            if current_image is None:
                continue

            # Check if the images are the same size
            if given_image.shape == current_image.shape:
                # Count the number of overlapping pixels
                overlap = np.sum(given_image == current_image)

                # Update the maximum overlap and the path of the most similar image
                if overlap > max_overlap:
                    max_overlap = overlap
                    most_similar_image_path = file_path
                
        nums.append(int(most_similar_image_path.split('.')[0].split('/')[-1]))

    return nums

# Example usage:
def get_cols_rows(image_path):
    directory_path = 'nums'  # Replace with your directory path
    desired_color = [81, 81, 81]  # Replace with your desired BGR color

    print("LOADING:", image_path)
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    output_folder = 'debugs/better/row'  # Replace with your desired output folder
    point = (10, h - 70)  # Replace with your reference point coordinates
    extracts = replace_and_save_contiguous(image_path, desired_color, point, output_folder)
    rows = find_most_overlapping_image(directory_path, extracts)
    # print('row', rows)

    output_folder = 'debugs/better/col'  # Replace with your desired output folder
    point = (700, 0)  # Replace with your reference point coordinates
    extracts = replace_and_save_contiguous(image_path, desired_color, point, output_folder)
    cols = find_most_overlapping_image(directory_path, extracts)
    # print('col', cols)

    return (cols, rows)

# image_path = 'imgs/Screen Shot 2023-12-17 at 12.59.32 PM.png'  # Replace with your image path
# get_cols_rows(image_path)
