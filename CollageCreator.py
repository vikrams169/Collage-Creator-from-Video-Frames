# Vikram Setty (2018MED1010)

# Computer Vision (CS518) - Assignment 1

# To Execute the Code, Initially Run the Code Block Commented Out Below to get the Image Frames from the Video into a Directory. Then Run this Python3 File like 'python3 CollageCreator.py' for example in an Ubuntu OS.

'''

# Function for Extracting all the Frames from the Video (at 1 FPS)

# Video taken from YouTube. Link: https://www.youtube.com/watch?v=VUs_iPB-PDw

# Name of the Video: 'skatebaording_video.mp4' & name of the Directory to Save the Frames to: 'image_frames'

# Run this to get the Frames into the Directory. Commented Out Since this is is not a Part of the Assignment.

import cv2
video_name = "skateboarding_video.mp4"
vidcap = cv2.VideoCapture(video_name)
success,image = vidcap.read()
count = 0
while success:
  vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
  cv2.imwrite("image_frames/frame%d.jpg" % count, cv2.resize(image, (600,450)))      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1

'''

# Importing all the Required Libraries
import os
import numpy as np
import skimage
from skimage import io
from skimage.color import rgb2gray
from skimage import filters
from skimage import feature
import matplotlib.pyplot as plt
import random


# Function for getting all the Images from the Directory into an Iterable List (Preferably Initially Empty)
def load_frames(directory):
  img_list = []
  for file in os.listdir(directory):
    img = io.imread(os.path.join(directory,file))
    if img is not None:
      img_list.append(img)
  return img_list


# Getting the Color Variation in an RGB Image (Each Channel Considered Independently) based on Variance from it's Histogram
def image_colour_variance(rgb_image):
  mean, var = [], []
  for i in range(3):
    channel = rgb_image[:,:,i]/255
    histogram, bin_edges = np.histogram(channel, bins=256, range=(0, 1))
    mean.append(np.mean(histogram))
    var.append(np.var(histogram))
  return var[0]/3  + var[1]/3 + var[2]/3 + ((mean[0])**2 - (np.mean(mean))**2) + ((mean[1])**2 - (np.mean(mean))**2) + ((mean[2])**2 - (np.mean(mean))**2)


# Analysing the Number of Edge Pixes in an RGB Image
def edge_information(rgb_image):
	edgeMapCanny = feature.canny(rgb2gray(rgb_image))
	return int(np.sum(edgeMapCanny == 1))


# Analysing the Corner Pixel Intensity Throughout the Image Using the FAST Method
def corner_information(rgb_image):
 	cornerMap = feature.corner_fast(rgb2gray(rgb_image))
 	return int(np.sum(cornerMap))


# Extracting the Colour Intensity Variance, Edge, and Corner Information for a Set of Extracted Images
def extract_image_info(rgb_images):
	colour_variance, edge_info, corner_info = [], [], []
	for image in rgb_images:
		colour_variance.append(image_colour_variance(image))
		edge_info.append(edge_information(image))
		corner_info.append(corner_information(image))
	return colour_variance, edge_info, corner_info


# Choosing 6 Random Images (as per the Specified Instructions) and Getting Their Information
def preprocessing(img_list):
	frames_random = []
	count_random = 0
	while True:
	  random_number = random.randint(0,len(img_list)-1)
	  if random_number not in frames_random:
	    frames_random.append(random_number)
	    count_random += 1
	  if count_random == 6:
	    break
	images = []
	for i in range(6):
	  images.append(img_list[frames_random[i]])
	colour_variance, edge_info, corner_info = extract_image_info(images)
	return images, colour_variance, edge_info, corner_info


# Assigning an Index to each Image (Their Position in the Collage Based on the Info Extracted). The Index Positions Look Like (in a 2*3 Grid):
# 0 1 2
# 3 4 5
def assign_index(colour_variance, edge_info, corner_info):
	index_list = [6, 6, 6, 6, 6, 6]
	max_colour_variance_1 = np.argmax(np.array(colour_variance))
	colour_variance[max_colour_variance_1] = 0
	max_colour_variance_2 = np.argmax(np.array(colour_variance))
	if edge_info[max_colour_variance_1] >= edge_info[max_colour_variance_2]:
		index_list[1] = max_colour_variance_1
		index_list[4] = max_colour_variance_2
	else:
		index_list[1] = max_colour_variance_2
		index_list[4] = max_colour_variance_1
	corner_info[max_colour_variance_1] = 0
	corner_info[max_colour_variance_2] = 0
	max_corners_1 = np.argmax(np.array(corner_info))
	corner_info[max_corners_1] = 0
	max_corners_2 = np.argmax(np.array(corner_info))
	if edge_info[max_corners_1] >= edge_info[max_corners_2]:
		index_list[0] = max_corners_1
		index_list[2] = max_corners_2
	else:
		index_list[0] = max_corners_2
		index_list[2] = max_corners_1
	corner_info[max_corners_1] = 0
	corner_info[max_corners_2] = 0
	max_corners_11 = np.argmax(np.array(corner_info))
	corner_info[max_corners_1] = 0
	max_corners_22 = np.argmax(np.array(corner_info))
	if edge_info[max_corners_11] >= edge_info[max_corners_22]:
		index_list[3] = max_corners_11
		index_list[5] = max_corners_22
	else:
		index_list[3] = max_corners_22
		index_list[5] = max_corners_11
	return index_list


# Placing the Images Next to Eachother based on the Indicies Decided
def place_images(images, index_list):
	image_collection = []
	for i in range(6):
		for j in range(6):
			if index_list[j] == i:
				image_collection.append(images[j])
	horizontal_1 = np.hstack([image_collection[0], image_collection[1], image_collection[2]])
	horizontal_2 = np.hstack([image_collection[3], image_collection[4], image_collection[5]])
	collage_image = np.vstack([horizontal_1, horizontal_2])
	return collage_image


# Function to Create the Collage
def CollageCreate(directory):
	img_list = load_frames(directory)
	images, colour_variance, edge_info, corner_info = preprocessing(img_list)
	index_list = assign_index(colour_variance, edge_info, corner_info)
	collage_image = place_images(images, index_list)
	io.imshow(collage_image)
	io.imsave('Collage.jpg',collage_image)
	return collage_image


if __name__ == '__main__':

	CollageCreate('image_frames')