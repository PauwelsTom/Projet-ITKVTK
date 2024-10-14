import itk
import numpy as np

# Définir les types pour les images 2D et les transformations affines
PixelType = itk.F
Dimension = 2
ImageType = itk.Image[PixelType, Dimension]
TransformType = itk.AffineTransform[PixelType, Dimension]
OptimizerType = itk.RegularStepGradientDescentOptimizerv4[PixelType]
MetricType = itk.MeanSquaresImageToImageMetricv4[ImageType, ImageType]
RegistrationType = itk.ImageRegistrationMethodv4[ImageType, ImageType, TransformType]
ResampleFilterType = itk.ResampleImageFilter[ImageType, ImageType]

# Charger les scans 3D
scan1 = itk.imread('Data/case6_gre1.nrrd', PixelType)
scan2 = itk.imread('Data/case6_gre2.nrrd', PixelType)

# Convertir en numpy pour manipulation facile
scan1_np = itk.GetArrayViewFromImage(scan1)
scan2_np = itk.GetArrayViewFromImage(scan2)

# Initialiser les images 3D pour les résultats
registered_scan2 = np.zeros_like(scan2_np)

# Registration slice par slice
for i in range(scan1_np.shape[0]):
    fixed_slice = scan1_np[i, :, :]
    moving_slice = scan2_np[i, :, :]

    fixed_image = itk.image_from_array(fixed_slice, is_vector=False)
    moving_image = itk.image_from_array(moving_slice, is_vector=False)
    
    # Initialisation de la transformation affine
    initial_transform = TransformType.New()
    
    # Configurer le composant de registration
    registration = RegistrationType.New()
    registration.SetFixedImage(fixed_image)
    registration.SetMovingImage(moving_image)
    registration.SetInitialTransform(initial_transform)
    
    # Configurer le métrique et l'optimiseur
    metric = MetricType.New()
    optimizer = OptimizerType.New()
    optimizer.SetNumberOfIterations(200)
    optimizer.SetLearningRate(1.0)
    optimizer.SetMinimumStepLength(0.001)
    
    registration.SetMetric(metric)
    registration.SetOptimizer(optimizer)
    
    # Effectuer la registration
    registration.Update()
    
    # Appliquer la transformation au slice en déplacement
    resample = ResampleFilterType.New()
    resample.SetInput(moving_image)
    resample.SetTransform(registration.GetModifiableTransform())
    resample.SetUseReferenceImage(True)
    resample.SetReferenceImage(fixed_image)
    resample.Update()
    
    resampled_slice = itk.array_from_image(resample.GetOutput())
    registered_scan2[i, :, :] = resampled_slice

# Convertir le résultat en image ITK et sauvegarder
registered_scan2_image = itk.image_from_array(registered_scan2, is_vector=False)
itk.imwrite(registered_scan2_image, 'registered_case6_gre2.nrrd')
