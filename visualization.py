import vtk

def visualize_changes(fixed_image_path, moving_image_path):
    fixed_image = vtk.vtkNrrdReader()
    fixed_image.SetFileName(fixed_image_path)
    fixed_image.Update()

    moving_image = vtk.vtkNrrdReader()
    moving_image.SetFileName(moving_image_path)
    moving_image.Update()
    
    diff_filter = vtk.vtkImageMathematics()
    diff_filter.SetOperationToSubtract()
    diff_filter.SetInput1Data(fixed_image.GetOutput())
    diff_filter.SetInput2Data(moving_image.GetOutput())
    diff_filter.Update()

    volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
    volume_mapper.SetInputConnection(diff_filter.GetOutputPort())
    
    color_transfer_function = vtk.vtkColorTransferFunction()
    color_transfer_function.AddRGBPoint(-1000, 0.0, 0.0, 1.0)
    color_transfer_function.AddRGBPoint(0, 1.0, 1.0, 1.0)
    color_transfer_function.AddRGBPoint(1000, 1.0, 0.0, 0.0)

    opacity_transfer_function = vtk.vtkPiecewiseFunction()
    opacity_transfer_function.AddPoint(-1000, 0.0)
    opacity_transfer_function.AddPoint(0, 0.5)
    opacity_transfer_function.AddPoint(1000, 1.0)
    
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_transfer_function)
    volume_property.SetScalarOpacity(opacity_transfer_function)
    volume_property.ShadeOn()
    volume_property.SetInterpolationTypeToLinear()
    
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)
    
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    
    render_window.SetOffScreenRendering(1)
    
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    render_window.SetInteractor(interactor)
    
    renderer.AddVolume(volume)
    renderer.SetBackground(0, 0, 0)
    
    render_window.Render()
    
    render_window.SetOffScreenRendering(0)
    
    interactor.Start()