#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import glob
    import os
    import pathlib

    # Import special modules ...
    try:
        import cartopy
        cartopy.config.update(
            {
                "cache_dir" : pathlib.PosixPath("~/.local/share/cartopy").expanduser(),
            }
        )
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import geojson
    except:
        raise Exception("\"geojson\" is not installed; run \"pip install --user geojson\"") from None
    try:
        import matplotlib
        matplotlib.rcParams.update(
            {
                            "backend" : "Agg",                                  # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
                         "figure.dpi" : 300,
                     "figure.figsize" : (9.6, 7.2),                             # NOTE: See https://github.com/Guymer/misc/blob/main/README.md#matplotlib-figure-sizes
                          "font.size" : 8,
                "image.interpolation" : "none",
                     "image.resample" : False,
            }
        )
        import matplotlib.pyplot
    except:
        raise Exception("\"matplotlib\" is not installed; run \"pip install --user matplotlib\"") from None
    try:
        import shapely
        import shapely.geometry
    except:
        raise Exception("\"shapely\" is not installed; run \"pip install --user Shapely\"") from None

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.geo
        import pyguymer3.image
        import pyguymer3.media
    except:
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

    # **************************************************************************

    # Create argument parser and parse the arguments ...
    parser = argparse.ArgumentParser(
           allow_abbrev = False,
            description = "Make maps using old Cartopy.",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action = "store_true",
          help = "print debug messages",
    )
    args = parser.parse_args()

    # **************************************************************************

    # Create short-hands ...
    interpolation = "none"
    regrid_shape = 750
    resample = False

    # Loop over figure DPIs ...
    for dpi in [
         75,
        150,
        300,
        600,
    ]:
        # Initialize list ...
        pNames = []

        # Loop over background image resolutions ...
        for resolution in [
            "large0256px",
            "large0512px",
            "large1024px",
            "large2048px",
            "large4096px",
            "large8192px",
        ]:
            # Create short-hand and skip if the figure exists ...
            pName = f'{__file__.removesuffix(".py")}_dpi={dpi:d}_res={resolution}.png'
            pNames.append(pName)
            if os.path.exists(pName):
                continue

            print(f"Making \"{pName}\" ...")

            # Create figure ...
            fg = matplotlib.pyplot.figure(
                    dpi = dpi,
                figsize = (12.8, 7.2),
            )

            # Create axis ...
            ax = pyguymer3.geo.add_axis(
                fg,
                add_coastlines = False,
                 add_gridlines = True,
                         debug = args.debug,
            )

            # Configure axis ...
            pyguymer3.geo.add_map_background(
                ax,
                        debug = args.debug,
                interpolation = interpolation,
                         name = "natural-earth-1",
                 regrid_shape = regrid_shape,
                     resample = resample,
                   resolution = resolution,
            )

            # Loop over GeoJSON files ...
            for jName in sorted(glob.glob(os.path.abspath(f"{pyguymer3.__path__[0]}/../tests/greatCircle/greatCircle?_4.geojson"))):
                print(f"Loading \"{jName}\" ...")

                # Load GeoJSON file ...
                with open(jName, "rt", encoding = "utf-8") as fObj:
                    savedCircle = shapely.geometry.shape(geojson.load(fObj))

                # Plot saved great circle ...
                ax.add_geometries(
                    pyguymer3.geo.extract_lines(savedCircle),
                    cartopy.crs.PlateCarree(),
                        color = "none",
                    edgecolor = "red",
                    linewidth = 1.0,
                )

            # Configure axis ...
            ax.set_title(f"interpolation = \"{interpolation}\"; regrid_shape = {regrid_shape:d}; resample = {repr(resample)}")

            # Configure figure ...
            fg.suptitle(f"{fg.get_size_inches()[0]:.1f} inches × {fg.get_size_inches()[1]:.1f} inches at {dpi:d} DPI with \"{resolution}\" background image")
            fg.tight_layout()

            # Save figure ...
            fg.savefig(pName)
            matplotlib.pyplot.close(fg)

            # Optimise figure ...
            pyguymer3.image.optimise_image(
                pName,
                  debug = args.debug,
                  strip = True,
                timeout = 3600.0,
            )

        # **********************************************************************

        # Create short-hand ...
        wName = f'{__file__.removesuffix(".py")}_dpi={dpi:d}_fullSize.webp'

        # Check if WEBP needs making ...
        if not os.path.exists(wName):
            print(f"Making \"{wName}\" ...")

            # Make 1 fps WEBP ...
            pyguymer3.media.images2webp(
                pNames,
                wName,
                fps = 1.0,
            )

        # Loop over maximum sizes ...
        for maxSize in [
             256,
             512,
            1024,
            2048,
            4096,
            8192,
        ]:
            # Skip this size if it is larger than the figure ...
            if maxSize >= round(12.8 * dpi):
                continue

            # Create short-hand ...
            wName = f'{__file__.removesuffix(".py")}_dpi={dpi:d}_{maxSize:04d}px.webp'

            # Check if WEBP needs making ...
            if not os.path.exists(wName):
                print(f"Making \"{wName}\" ...")

                # Make 1 fps WEBP ...
                pyguymer3.media.images2webp(
                    pNames,
                    wName,
                             fps = 1.0,
                    screenHeight = maxSize,
                     screenWidth = maxSize,
                )
