# Study Images In Cartopy

!["mypy" GitHub Action Status](https://github.com/Guymer/studyImagesInCartopy/actions/workflows/mypy.yaml/badge.svg) !["pylint" GitHub Action Status](https://github.com/Guymer/studyImagesInCartopy/actions/workflows/pylint.yaml/badge.svg)

This repository contains a collection of scripts to study rendering images in Cartopy.

With the new functionality in Cartopy, picking the best parameters to render an image in Cartopy is a seven-dimensional problem. To help collapse the parameter-space then I will make the following assumptions:

* `dpi = 300`;
* `resample = False`; and
* if rendering tiles then the tile provider is Thunderforest and `scale = 2`.

Bearing that in mind, then the problem becomes *only* four-dimensional. The following choices have been made (in order):
1. `interpolation = "gaussian"` (see [MatPlotLib documentation for interpolations for `imshow()`](https://matplotlib.org/stable/gallery/images_contours_and_fields/interpolation_methods.html));
2. `regrid_shape = ×2.0` (sometimes ×4.0 is better but the RAM requirements are prohibitive for universal usage ... maybe);
3. `resolution = "large4096px"` (depends on `regrid_shape`);
4. when calculating a tile zoom level based off a map's resolution `res = ×2.0` (compare the contour lines between "bicubic" and "gaussian" for the Norway tile example).

## Dependencies

This collection requires the following Python modules to be installed and available in your `PYTHONPATH`.

* [cartopy](https://pypi.org/project/Cartopy/)
* [geojson](https://pypi.org/project/geojson/)
* [matplotlib](https://pypi.org/project/matplotlib/)
* [PIL](https://pypi.org/project/Pillow/)
* [pyguymer3](https://github.com/Guymer/PyGuymer3)
* [shapely](https://pypi.org/project/Shapely/)
