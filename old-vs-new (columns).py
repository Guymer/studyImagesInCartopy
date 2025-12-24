#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import os

    # Import special modules ...
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
        import PIL
        import PIL.Image
        import PIL.ImageDraw
        import PIL.ImageFont
        PIL.Image.MAX_IMAGE_PIXELS = 1024 * 1024 * 1024                         # [px]
    except:
        raise Exception("\"PIL\" is not installed; run \"pip install --user Pillow\"") from None

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.image
    except:
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

    # **************************************************************************

    # Create argument parser and parse the arguments ...
    parser = argparse.ArgumentParser(
           allow_abbrev = False,
            description = "Make images comparing maps using old Cartopy and maps using new Cartopy.",
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
    padding = 32                                                                # [px]
    snippet = 256                                                               # [px]
    snippetScale = 4                                                            # [×]
    title = 128                                                                 # [px]

    # Create short-hands ...
    fontPath = matplotlib.font_manager.findfont("DejaVu Sans")
    fontSize = title // 4                                                       # [px]
    font = PIL.ImageFont.truetype(fontPath, fontSize)

    print(f"INFO: Will use \"{fontPath}\" at {fontSize:d} px.")

    # Loop over figure DPIs ...
    for dpi in [
         75,
        150,
        300,
        600,
    ]:
        # Loop over safety factors ...
        for sf in [
            0.25,
            0.5,
            1.0,
            2.0,
            4.0,
        ]:
            # Create short-hand and skip if the figure exists ...
            dName = f'{__file__.removesuffix(".py")}/dpi={dpi:d}'
            if not os.path.exists(dName):
                os.makedirs(dName)
            pName1 = f"{dName}/sf={sf:4.2f}.png"
            if os.path.exists(pName1):
                continue

            print(f"Making \"{pName1}\" ...")

            # Create the PIL image and drawing object ...
            img = PIL.Image.new(
                color = (255, 255, 255),
                 mode = "RGB",
                 size = (
                    2 * (snippetScale * snippet + 2 * padding),
                    title + 6 * (snippetScale * snippet + 2 * padding + title),
                ),
            )
            draw = PIL.ImageDraw.Draw(img)

            # Calculate the regrid shape based off the resolution and the size
            # of the figure, as well as a safety factor (remembering Nyquist) ...
            regrid_shape = (
                round(sf * 12.8 * dpi),
                round(sf *  7.2 * dpi),
            )                                                                   # [px], [px]

            # Draw title ...
            draw.text(
                (
                    img.width // 2,
                    title // 2,
                ),
                f"12.8 inches × 7.2 inches at {dpi:d} DPI\nresample = False",
                anchor = "ms",          # See https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
                  fill = (0, 0, 0),
                  font = font,
            )

            # Loop over background image resolutions ...
            for iResolution, resolution in enumerate(
                [
                    "large0256px",
                    "large0512px",
                    "large1024px",
                    "large2048px",
                    "large4096px",
                    "large8192px",
                ]
            ):
                # Create short-hands ...
                pName2 = f"old/dpi={dpi:d}/res={resolution}.png"
                pName3 = f"new/dpi={dpi:d}/sf={sf:4.2f}/res={resolution}.png"

                # **************************************************************

                # Create short-hands ...
                upper = 2 * title + padding + iResolution * (snippetScale * snippet + 2 * padding + title)  # [px]
                lower = upper + (snippetScale * snippet)                        # [px]
                left = padding                                                  # [px]
                right = left + (snippetScale * snippet)                         # [px]

                # Shade the region for this combination and draw title ...
                img.paste(
                    (223, 223, 223),
                    (
                        left - padding // 2,
                        upper - title - padding // 2,
                        right + padding // 2,
                        lower + padding // 2,
                    ),
                )
                draw.text(
                    (
                        (left + right) // 2,
                        upper - 3 * title // 4,
                    ),
                    f"interpolation = \"none\"\nregrid_shape = 750\nresolution = \"{resolution}\"",
                    anchor = "ms",      # See https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
                      fill = (0, 0, 0),
                      font = font,
                )

                print(f"  Loading \"{pName2}\" ...")

                # Load the PIL image ...
                with PIL.Image.open(pName2) as iObj:
                    # Paste the image after cutting out the middle and scaling
                    # it up ...
                    img.paste(
                        iObj.crop(
                            (
                                iObj.width  // 2 - snippet // 2,
                                iObj.height // 2 - snippet // 2,
                                iObj.width  // 2 + snippet // 2,
                                iObj.height // 2 + snippet // 2,
                            )
                        ).resize(
                            (
                                snippetScale * snippet,
                                snippetScale * snippet,
                            ),
                            PIL.Image.Resampling.NEAREST,
                        ),
                        (
                            left,
                            upper,
                            right,
                            lower,
                        ),
                    )

                # **************************************************************

                # Create short-hands ...
                upper = 2 * title + padding + iResolution * (snippetScale * snippet + 2 * padding + title)  # [px]
                lower = upper + (snippetScale * snippet)                        # [px]
                left = padding + (snippetScale * snippet + 2 * padding)         # [px]
                right = left + (snippetScale * snippet)                         # [px]

                # Shade the region for this combination and draw title ...
                img.paste(
                    (223, 223, 223),
                    (
                        left - padding // 2,
                        upper - title - padding // 2,
                        right + padding // 2,
                        lower + padding // 2,
                    ),
                )
                draw.text(
                    (
                        (left + right) // 2,
                        upper - 3 * title // 4,
                    ),
                    f"interpolation = \"bicubic\"\nregrid_shape = ({regrid_shape[0]:d},{regrid_shape[1]:d})\nresolution = \"{resolution}\"",
                    anchor = "ms",      # See https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
                      fill = (0, 0, 0),
                      font = font,
                )

                print(f"  Loading \"{pName3}\" ...")

                # Load the PIL image ...
                with PIL.Image.open(pName3) as iObj:
                    # Paste the image after cutting out the middle and scaling
                    # it up ...
                    img.paste(
                        iObj.crop(
                            (
                                iObj.width  // 2 - snippet // 2,
                                iObj.height // 2 - snippet // 2,
                                iObj.width  // 2 + snippet // 2,
                                iObj.height // 2 + snippet // 2,
                            )
                        ).resize(
                            (
                                snippetScale * snippet,
                                snippetScale * snippet,
                            ),
                            PIL.Image.Resampling.NEAREST,
                        ),
                        (
                            left,
                            upper,
                            right,
                            lower,
                        ),
                    )

            print(f"Saving \"{pName1}\" ...")

            # Save the image ...
            img.save(
                pName1,
                optimize = True,
            )

            # Optimise PNG ...
            pyguymer3.image.optimise_image(
                pName1,
                  debug = args.debug,
                  strip = True,
                timeout = 3600.0,
            )
