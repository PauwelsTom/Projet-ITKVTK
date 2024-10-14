import itk

def register_images(fixed_image_path, moving_image_path, output_image_path):
    PixelType = itk.F
    Dimension = 3
    ImageType = itk.Image[PixelType, Dimension]

    print(f"Lecture de l'image fixe depuis : {fixed_image_path}")
    fixed_image = itk.imread(fixed_image_path, PixelType)
    if fixed_image is None:
        raise ValueError(f"L'image fixe n'a pas pu être chargée depuis : {fixed_image_path}")

    print(f"Lecture de l'image mobile depuis : {moving_image_path}")
    moving_image = itk.imread(moving_image_path, PixelType)
    if moving_image is None:
        raise ValueError(f"L'image mobile n'a pas pu être chargée depuis : {moving_image_path}")

    print(f"Les images ont été chargées avec succès. Types : {type(fixed_image)}, {type(moving_image)}")

    fixed_image_cast = itk.cast_image_filter(fixed_image, ttype=(type(fixed_image), ImageType))
    moving_image_cast = itk.cast_image_filter(moving_image, ttype=(type(moving_image), ImageType))

    TransformType = itk.VersorRigid3DTransform[itk.D]
    initial_transform = TransformType.New()

    initializer = itk.CenteredTransformInitializer[TransformType, ImageType, ImageType].New(
        Transform=initial_transform,
        FixedImage=fixed_image_cast,
        MovingImage=moving_image_cast
    )
    initializer.InitializeTransform()

    optimizer = itk.RegularStepGradientDescentOptimizerv4.New()
    metric = itk.MeanSquaresImageToImageMetricv4[ImageType, ImageType].New()

    registration_method = itk.ImageRegistrationMethodv4.New()
    registration_method.SetFixedImage(fixed_image_cast)
    registration_method.SetMovingImage(moving_image_cast)
    registration_method.SetInitialTransform(initial_transform)
    registration_method.SetOptimizer(optimizer)
    registration_method.SetMetric(metric)

    print("Exécution du recalage...")
    registration_method.Update()

    final_transform = registration_method.GetTransform()

    resampler = itk.ResampleImageFilter.New()
    resampler.SetInput(moving_image_cast)
    resampler.SetTransform(final_transform)
    resampler.SetUseReferenceImage(True)
    resampler.SetReferenceImage(fixed_image_cast)
    resampler.SetInterpolator(itk.LinearInterpolateImageFunction.New())

    registered_image = resampler.GetOutput()

    print(f"Sauvegarde de l'image recalée vers : {output_image_path}")
    itk.imwrite(registered_image, output_image_path)

fixed_image_path = 'Data/case6_gre1.nrrd'
moving_image_path = 'Data/case6_gre2.nrrd'
output_image_path = 'Data/registered_image.nrrd'

register_images(fixed_image_path, moving_image_path, output_image_path)
