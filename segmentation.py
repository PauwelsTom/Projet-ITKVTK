import vtk
import numpy as np
import matplotlib.pyplot as plt
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import SimpleITK as sitk

fixed_image_path = 'Data/case6_gre1.nrrd'

def plot_histogram(image_path):
    reader = vtk.vtkNrrdReader()
    reader.SetFileName(image_path)
    reader.Update()

    image_data = reader.GetOutput()
    scalars = image_data.GetPointData().GetScalars()

    voxel_values = vtk_to_numpy(scalars)
    
    plt.hist(voxel_values, bins=50, color='gray')
    plt.title('Histogram of Voxel Intensities')
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.show()

def print_voxel_values(image_data, description):
    scalars = image_data.GetPointData().GetScalars()
    voxel_values = vtk_to_numpy(scalars)
    print(f"{description} - Min: {voxel_values.min()}, Max: {voxel_values.max()}, Mean: {voxel_values.mean()}")

def display_image(image_data, title="Image"):
    voxel_values = vtk_to_numpy(image_data.GetPointData().GetScalars())
    
    dims = image_data.GetDimensions()
    voxel_values = voxel_values.reshape(dims, order='F')
    
    middle_slice = voxel_values[:, :, dims[2]//2]
    
    plt.imshow(middle_slice, cmap='gray')
    plt.title(title)
    plt.show()

def save_image_as_nrrd(image_data, file_path):
    vtk_array = image_data.GetPointData().GetScalars()
    np_array = vtk_to_numpy(vtk_array)
    np_array = np_array.reshape(image_data.GetDimensions(), order='F')
    
    sitk_image = sitk.GetImageFromArray(np_array)
    
    spacing = image_data.GetSpacing()
    origin = image_data.GetOrigin()
    sitk_image.SetSpacing(spacing)
    sitk_image.SetOrigin(origin)
    
    sitk.WriteImage(sitk_image, file_path)

def segment_image(image_path, lower_threshold_value, upper_threshold_value, output_path):
    reader = vtk.vtkNrrdReader()
    reader.SetFileName(image_path)
    reader.Update()

    image_data = reader.GetOutput()
    print_voxel_values(image_data, "Original Image")

    gaussian_filter = vtk.vtkImageGaussianSmooth()
    gaussian_filter.SetInputConnection(reader.GetOutputPort())
    gaussian_filter.SetRadiusFactors(2, 2, 2)
    gaussian_filter.Update()

    smoothed_image = gaussian_filter.GetOutput()
    print_voxel_values(smoothed_image, "Smoothed Image")

    threshold_filter = vtk.vtkImageThreshold()
    threshold_filter.SetInputConnection(gaussian_filter.GetOutputPort())
    threshold_filter.ThresholdBetween(lower_threshold_value, upper_threshold_value)
    threshold_filter.ReplaceInOn()
    threshold_filter.SetInValue(1)
    threshold_filter.ReplaceOutOn()
    threshold_filter.SetOutValue(0)
    threshold_filter.Update()

    thresholded_image = threshold_filter.GetOutput()
    print_voxel_values(thresholded_image, "Thresholded Image")

    cast_filter = vtk.vtkImageCast()
    cast_filter.SetInputConnection(threshold_filter.GetOutputPort())
    cast_filter.SetOutputScalarTypeToUnsignedChar()
    cast_filter.Update()

    casted_image = cast_filter.GetOutput()
    print_voxel_values(casted_image, "Casted Image")

    permute_filter = vtk.vtkImagePermute()
    permute_filter.SetInputData(casted_image)
    permute_filter.SetFilteredAxes(2, 1, 0)
    permute_filter.Update()

    permuted_image = permute_filter.GetOutput()

    resample = vtk.vtkImageResample()
    resample.SetInputData(permuted_image)
    resample.SetOutputExtent(image_data.GetExtent())
    resample.SetOutputSpacing(image_data.GetSpacing())
    resample.SetOutputOrigin(image_data.GetOrigin())
    resample.Update()

    resampled_image = resample.GetOutput()
    
    display_image(resampled_image, "Segmented Image")
    
    save_image_as_nrrd(resampled_image, output_path)