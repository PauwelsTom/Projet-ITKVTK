import vtk
from segmentation import plot_histogram, segment_image
from visualization import visualize_changes
import os

fixed_image_path = 'Data/case6_gre1.nrrd'
moving_image_path = 'Data/case6_gre2.nrrd'
segmented_image_path = 'Data/segmented_image.nrrd'

def main():
    plot_histogram(fixed_image_path)
    
    lower_threshold_value = 50
    upper_threshold_value = 150
    segment_image(fixed_image_path, lower_threshold_value, upper_threshold_value, segmented_image_path)
    
    visualize_changes(fixed_image_path, moving_image_path)

if __name__ == "__main__":
    main()
