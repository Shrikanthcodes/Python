#Libraries used
import unittest
import os
import cv2
import numpy as np
from main import apply_operation, ImageOperation

class TestImageProcessing(unittest.TestCase):
    def setUp(self):
        self.input_image = cv2.imread('test_image.jpg', cv2.IMREAD_COLOR)
        self.assertIsNotNone(self.input_image, "Test image not found.")

    def test_resize_image(self):
        """
        Test the resize_image operation by comparing the output image's dimensions
        with the expected dimensions after resizing.
        """
        output_image = apply_operation(ImageOperation.RESIZE, self.input_image, scale_x=0.5, scale_y=0.5)
        self.assertIsNotNone(output_image)
        self.assertEqual(output_image.shape, (int(self.input_image.shape[0] * 0.5), int(self.input_image.shape[1] * 0.5), 3))

    def test_rotate_image(self):
        """
        Test the rotate_image operation by comparing the output image's dimensions
        with the expected dimensions after rotation.
        """
        output_image = apply_operation(ImageOperation.ROTATE, self.input_image, angle=90)
        self.assertIsNotNone(output_image)
        self.assertEqual(output_image.shape, (self.input_image.shape[1], self.input_image.shape[0], 3))

    def test_blur_image(self):
        """
        Test the blur_image operation by checking if the output image is not None
        and has the same dimensions as the input image.
        """
        output_image = apply_operation(ImageOperation.BLUR, self.input_image, kernel_size=3)
        self.assertIsNotNone(output_image)
        self.assertEqual(output_image.shape, self.input_image.shape)

    def test_histogram_equalization(self):
        """
        Test the histogram_equalization operation by checking if the output image
        is not None and has the same dimensions as the input image.
        """
        output_image = apply_operation(ImageOperation.HISTOGRAM_EQUALIZATION, self.input_image)
        self.assertIsNotNone(output_image)
        self.assertEqual(output_image.shape, self.input_image.shape)

    def test_image_filtering(self):
        """
        Test the image_filtering operation by checking if the output image is not None
        and has the same dimensions as the input image.
        """
        kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
        output_image = apply_operation(ImageOperation.IMAGE_FILTERING, self.input_image, kernel=kernel)
        self.assertIsNotNone(output_image)
        self.assertEqual(output_image.shape, self.input_image.shape)

    def test_image_thresholding(self):
        """
        Test the image_thresholding operation by checking if the output image is not None
        and has the same dimensions as the input image.
        """
        output_image = apply_operation(ImageOperation.IMAGE_THRESHOLDING, self.input_image, threshold=128, max_value=255)
        self.assertIsNotNone(output_image)
        self.assertEqual(output_image.shape, self.input_image.shape)

    def test_morphological_operations(self):
        """
        Test the morphological_operations (e.g., erosion) by checking if the output image
        is not None and has the same dimensions as the input image.
        """
        output_image = apply_operation(ImageOperation.MORPHOLOGICAL_OPERATIONS, self.input_image, operation="erode", kernel_size=3, iterations=1)
        self.assertIsNotNone(output_image)
        self.assertEqual(output_image.shape, self.input_image.shape)

if __name__ == '__main__':
    unittest.main()
