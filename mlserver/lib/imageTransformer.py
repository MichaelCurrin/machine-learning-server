# -*- coding: utf-8 -*-
"""Image Transformer application file.

The purpose of the ImageTransformer is to transform (resize, crop, etc)
images so that images meet the requirements so that the images can be
sent to plugins, or returned.

We use float division from Python 3.x instead of floor division, so scaling
factor results are kept as floats and not rounded down to zero as an integer.

Usage for testing:
    $ python -m lib.imageTransformer --help
"""
import os
import sys

from PIL import Image


class ImageTransformer(object):
    """Class for creating an image transformer instance, which is able contain
    an image and manipulate it.

    It is recommended to crop an image and the resize it (which also does some
    cropping). Doing both together should give an identical image, but
    doing resizing last ensures you always reach the target dimensions.
    """

    def __init__(self):
        """Initialise an instance of the ImageTransformer class."""
        self.image = None

    def setImage(self, imageInput, mode='RGB', convert=True):
        """
        Receive image then convert to Image object and store on instance.

        When done working with an ImageTransformer instance, it is
        recommended to use obj.image.close() to close the Image instance.

        @param imageInput: Image input as path to local image file as a string.
            Also accepts a readable file object in io.BytesIO format, but,
            then it is recommended to close that file object or use a with
            block so that it is removed from memory when no longer needed.
        @param mode: Default 'RGB'. Image mode (string) to convert to,
            provided that `convert` is True.
        @param convert: Default True. Boolean flag to convert image
            to required mode.

        @return: None
        """
        if isinstance(imageInput, str):
            assert os.access(imageInput, os.R_OK), (
                'Unable to read path to image: `{0}`.'.format(imageInput)
            )
        image = Image.open(imageInput)
        self.image = image.convert(mode) if convert else image

    def getImage(self):
        """Return the image stored on the instance.

        It is recommended to close the image object after getting the image
        from the Image Transformer.

        @return: the image in the most recent state, either the original or
            as modified.
        """
        return self.image

    def removeTransparency(self, bgColor=(255, 255, 255, 255)):
        """Remove transparent background from PNG images and converts to RGB
        format.

        @param bgColor: Background value to be used on replacing background
            transparency of a PNG, as a tuple of 4 values from 0 to 255.

        @return: None
        """
        img = self.image

        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and
                                          'transparency' in img.info):
            alpha = img.convert('RGBA').split()[-1]
            bg = Image.new("RGBA", img.size, bgColor)
            # Place original image on solid background.
            bg.paste(img, mask=alpha)
            img = bg.convert('RGB')
        else:
            img = img.convert('RGB')

        # Overwrite image with the modified one with transparency removed.
        self.image = img

    def specialCrop(self, xCoord, yCoord, scaleFactorW, scaleFactorH,
                    minWidth=1, minHeight=1):
        """Crop an image around (X,Y) point coordinates to a fraction of the
        actual image dimensions.

        A co-ordinate point must be specified as a co-ordinate pair of values,
        each on a percetnage scale exlcuding zero. i.e. from 1 to 100.

        A crop factor must be supplied to indicate how much of the image
        should be removed on cropping, where 0.9 would be 90% of the original
        image.

        @param xCoord: X co-ordinate of type int, or value which can be cast
            to an int.
        @param yCoord: Y co-ordinate of type int, or value which can be cast
            to an int.
        @param scaleFactorW: The target width crop factor, of type float.
        @param scaleFactorH: The target height crop factor, of type float.
        @param minWidth: Minimum image pixel width to crop to, to avoid getting
            width of zero when cropping by a small percentage value on a
            small image. Defaults to 1 if None.
        @param minHeight: Minimum image pixel height to crop to. Defaults to
            1 if None.

        @return: None
        """
        if minWidth is None or minHeight is None:
            minWidth = minHeight = 1

        xCoord = int(xCoord)
        yCoord = int(yCoord)

        assert 0 <= xCoord <= 100, (
            'Expected the X co-ordinate {0} to be between 0 and 100.'
            .format(xCoord)
        )
        assert 0 <= yCoord <= 100, (
            'Expected the Y co-ordinate {0} to be between 0 and 100.'
            .format(xCoord)
        )

        assert isinstance(scaleFactorW, float), (
            'Expected scaleFactorW to be type `float`, but got type `{0}`.'
            .format(type(scaleFactorW).__name__)
        )
        assert isinstance(scaleFactorH, float), (
            'Expected scaleFactorH to be type `float`, but got type `{0}`.'
            .format(type(scaleFactorH).__name__)
        )

        img = self.image
        w = img.size[0]
        h = img.size[1]

        # Convert co-ordinates (percentage values) into pixel values.
        xPx = int(xCoord / 100 * w)
        yPx = int(yCoord / 100 * h)

        targetW = max(int(scaleFactorW * w), minWidth)
        targetH = max(int(scaleFactorH * h), minHeight)

        # Get pixels for the corners of the cropped image box.
        bStartX = xPx - (targetW / 2)
        bEndX = xPx + (targetW / 2)
        bStartY = yPx - (targetH / 2)
        bEndY = yPx + (targetH / 2)

        # Bring the target box corners back within the original image area if
        # the mark was placed too close to the original image borders.
        # Otherwise we end up with a part the original image surrounded
        # by next to a black area.
        if bStartX < 0:
            bEndX = bEndX + abs(bStartX)
            bStartX = 0

        if bEndX > w:
            bStartX = bStartX - abs(w - bEndX)
            bEndX = w

        if bStartY < 0:
            bEndY = bEndY + abs(bStartY)
            bStartY = 0

        if bEndY > h:
            bEndY = h
            bStartY = bStartY - abs(h - bEndY)

        self.image = img.crop((bStartX, bStartY, bEndX, bEndY))

    def specialResize(self, targetWidth, targetHeight):
        """
        Resize image without distorting it.

        We calculate aspect ratio as width divided by height to do the
        resizing. If the target width and height are supplied for a
        rectangle or a square, either way we take off part of the image
        to get to the target size, but without distorting the image.
        i.e. resizing a landscape image to a square will remove the left
        and right sides, instead of squashing all info in the original image
        into a square. Note that the thinner the original image before
        cropped to a square, the more info on the sides of the target
        square which will be lost.

        @param targetWidth: the width in pixels of the resized image, as
            type int.
        @param targetHeight: the height in pixels of the resized image, as
            type int.

        @return: None
        """
        assert isinstance(targetWidth, int), (
            'Expected targetWidth as type `int` but got type `{0}`.'
            .format(type(targetWidth).__name__)
        )
        assert isinstance(targetHeight, int), (
            'Expected targetHeight as type `int` but got type `{0}`.'
            .format(type(targetHeight).__name__)
        )

        img = self.image
        w = img.size[0]
        h = img.size[1]

        originalAspectRatio = w / h
        targetAspectRatio = targetWidth / targetHeight

        if targetAspectRatio != originalAspectRatio:
            if targetAspectRatio > originalAspectRatio:
                # Image is too tall so take some off the top and bottom.
                scaleFactor = targetWidth / w
                cropSizeWidth = w
                cropSizeHeight = targetHeight / scaleFactor
                topCutLine = (h - cropSizeHeight) / 2

                sides = (0, topCutLine, cropSizeWidth,
                         topCutLine + cropSizeHeight)
            else:
                # Image is too wide so take some off the sides.
                scaleFactor = targetHeight / h
                cropSizeWidth = targetWidth / scaleFactor
                cropSizeHeight = h
                sideCutLine = (w - cropSizeWidth) / 2

                sides = (sideCutLine, 0, sideCutLine + cropSizeWidth,
                         cropSizeHeight)
            boxCorners = tuple(int(round(n)) for n in sides)
            img = img.crop(boxCorners)

        img = img.resize((targetWidth, targetHeight), Image.ANTIALIAS)

        # Overwrite the image with the resized and possibly cropped version.
        self.image = img


def test(args):
    """Test function for internal use when running script directly.

    Does a test on an input image path to perform cropping and resizing on it.
    Transparent backgrounds are removed for PNGs.

    Saves the modified images to the same directory as the image path but
    with a different filename.
    """
    if not args or set(args) & set(('-h', '--help')):
        print("Usage: python -m lib.imageTransformer [IMAGE_PATH] [-h|--help]")
        print("IMAGE_PATH: path to file image to transform.")
    else:
        imgPath = args[0]
        imgTr = ImageTransformer()
        imgTr.setImage(imgPath)

        # Remove background transparency.
        if imgTr.getImage().format == 'PNG':
            print("Remove transparency.")
            imgTr.removeTransparency()
            img = imgTr.getImage()
            # Use original path but add in text before the extension.
            newPath = "{0}_SOLID_BG.png".format(imgPath.rsplit('.', 1)[0])
            print(" - writing out to: {0}".format(newPath))
            img.save(newPath, format='png')

        # Crop the image and write out.
        print("Crop.")
        # Place mark at centre of image.
        x = 50
        y = 50
        # Crop to 40 % of original.
        cropFactor = 0.4
        imgTr.specialCrop(x, y, cropFactor, cropFactor)

        img = imgTr.getImage()
        newPath = "{0}_CROP.jpeg".format(imgPath.rsplit(".", 1)[0])
        print(" - writing out to: {0}".format(newPath))
        img.save(newPath, format='jpeg')

        # Resize the cropped image and write out.
        print("Resize.")
        targetH = 299
        targetW = 299
        imgTr.specialResize(targetH, targetW)

        img = imgTr.getImage()
        newPath = "{0}_CROP_THEN_RESIZE.jpeg".format(imgPath.rsplit('.', 1)[0])
        print(" - writing out to: {0}".format(newPath))
        img.save(newPath, format='jpeg')


if __name__ == '__main__':
    test(sys.argv[1:])
