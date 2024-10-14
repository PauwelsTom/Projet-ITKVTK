# Étude Longitudinale de l'Évolution d'une Tumeur

## Introduction

Ce projet utilise ITK et VTK pour analyser les changements d'une tumeur à partir de deux scans.

## Structure du Projet

main.py : Point d'entrée du projet
registration.py : Recalage des images
segmentation.py : Segmentation des tumeurs
visualization.py : Visualisation des changements
Data/ : Contient les images de scan

## Installation

pip install itk vtk

## Utilisation

python3 main.py

## Résultats

1. Recalage d'images

Le recalage d'images ne s'est pas avéré facile. Nous n'avons pas réussi à trouver une solution fonctionnelle pour obtenir une fonction de registration efficace, en raison d'un problème de type lors de la définition des images. Nous avons d'abord tenté d'utiliser les données des scans telles quelles en 3D, sans succès. Nous nous sommes ensuite tournés vers une autre méthode, consistant à décomposer le scan 3D en tranches (images en 2D) pour travailler sur chacune de ces tranches séparément, mais cela n'a pas fonctionné non plus. Cela se répercute inévitablement sur notre segmentation.

2. Segmentation des tumeurs

Nous avons réussi à effectuer une segmentation (voir segmented_image.nrrd). Malheureusement, nous n'avons pas réussi à afficher la segmentation avec notre fonction de visualisation des différences. Il est néanmoins possible de visualiser la segmentation avec un logiciel de visualisation d'images médicales ou avec l'extension VS Code "NiiVue". La segmentation n'est pas parfaite, mais nous parvenons à extraire quelques zones dans le cerveau.

3. Analyse des résultats

Nos résultats ne nous permettent pas de faire une analyse correcte.

4. Visualisation des changements

Nous avons réussi à réaliser une visualisation fonctionnelle avec les outils de VTK, permettant de voir les scans en trois dimensions. Voici les différentes étapes de notre fonction de visualisation :
    Lecture des images fixes et mobiles : Les images volumétriques sont lues à partir de fichiers NRRD à l'aide de vtk.vtkNrrdReader.
    Calcul de la différence : La différence entre les deux images est calculée à l'aide de vtk.vtkImageMathematics avec l'opération de soustraction.
    Création du mapper : vtk.vtkGPUVolumeRayCastMapper est utilisé pour mapper les données de volume, ce qui permet le rendu de volume avec l'accélération GPU.
    Définition des fonctions de transfert : Les fonctions de transfert de couleur et d'opacité sont définies pour mapper les valeurs scalaires aux couleurs et aux opacités.
    Configuration de la propriété du volume : vtk.vtkVolumeProperty est utilisé pour définir les propriétés de rendu du volume, y compris les fonctions de transfert de couleur et d'opacité, l'ombrage et le type d'interpolation.
    Création du volume : vtk.vtkVolume est créé et configuré avec le mapper et la propriété du volume.
    Configuration du renderer, de la fenêtre de rendu et de l'interacteur : Le renderer (vtk.vtkRenderer), la fenêtre de rendu (vtk.vtkRenderWindow) et l'interacteur (vtk.vtkRenderWindowInteractor) sont configurés pour permettre le rendu et l'interaction avec la scène 3D.
    Ajout du volume au renderer et rendu de la scène : Le volume est ajouté au renderer, et la scène est rendue avec render_window.Render(), après quoi l'interaction est lancée avec interactor.Start().

## Contributions

    Samuel Michaud
    Tom Pauwels