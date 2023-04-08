#Libraries used
import cv2
import numpy as np
import concurrent.futures
import os
import argparse
from enum import Enum
from queue import Queue


class ImageOperation(Enum):
    RESIZE = 1
    ROTATE = 2
    BLUR = 3
    CANNY = 4
    CONTRAST_BRIGHTNESS = 5
    HISTOGRAM_EQUALIZATION = 6
    FILTER = 7
    THRESHOLD = 8
    EROSION = 9
    DILATION = 10


def histogram_equalization(input_image):
    """
    Apply histogram equalization to an image to improve its contrast.
    
    :param input_image: The input image as a NumPy array.
    :return: The image with equalized histogram as a NumPy array.
    """
    if len(input_image.shape) == 3:
        ycrcb = cv2.cvtColor(input_image, cv2.COLOR_BGR2YCrCb)
        channels = cv2.split(ycrcb)
        cv2.equalizeHist(channels[0], channels[0])
        ycrcb = cv2.merge(channels)
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    else:
        return cv2.equalizeHist(input_image)


def filter_image(input_image, kernel):
    """
    Apply a custom filter to an image using the given kernel.
    
    :param input_image: The input image as a NumPy array.
    :param kernel: The custom kernel for the filter.
    :return: The filtered image as a NumPy array.
    """
    return cv2.filter2D(input_image, -1, kernel)


def threshold_image(input_image, threshold_value):
    """
    Apply binary thresholding to an image using the given threshold value.
    
    :param input_image: The input image as a NumPy array.
    :param threshold_value: The threshold value for binary thresholding.
    :return: The thresholded image as a NumPy array.
    """
    _, thresh = cv2.threshold(input_image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresh


def erosion_image(input_image, kernel_size, iterations):
    """
    Apply the erosion morphological operation to an image using the given kernel size and number of iterations.
    
    :param input_image: The input image as a NumPy array.
    :param kernel_size: The size of the structuring element for the erosion operation.
    :param iterations: The number of times the operation is applied.
    :return: The eroded image as a NumPy array.
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(input_image, kernel, iterations=iterations)


def dilation_image(input_image, kernel_size, iterations):
    """
    Apply the dilation morphological operation to an image using the given kernel size and number of iterations.
    
    :param input_image: The input image as a NumPy array.
    :param kernel_size: The size of the structuring element for the dilation operation.
    :param iterations:param iterations: The number of times the operation is applied.
    :return: The dilated image as a NumPy array.
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(input_image, kernel, iterations=iterations)

def resize_image(input_image, scale_x, scale_y):
    """
    Resize an image using the given scaling factors for x and y axes.
    
    :param input_image: The input image as a NumPy array.
    :param scale_x: The scaling factor for the x-axis.
    :param scale_y: The scaling factor for the y-axis.
    :return: The resized image as a NumPy array.
    """
    return cv2.resize(input_image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)


def rotate_image(input_image, angle):
    """
    Rotate an image by the given angle.
    
    :param input_image: The input image as a NumPy array.
    :param angle: The rotation angle in degrees.
    :return: The rotated image as a NumPy array.
    """
    rows, cols = input_image.shape[:2]
    center = (cols / 2, rows / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    return cv2.warpAffine(input_image, rotation_matrix, (cols, rows))


def blur_image(input_image, kernel_size):
    """
    Apply a Gaussian blur to an image using the given kernel size.
    
    :param input_image: The input image as a NumPy array.
    :param kernel_size: The size of the Gaussian kernel.
    :return: The blurred image as a NumPy array.
    """
    return cv2.blur(input_image, (kernel_size, kernel_size))


def canny_image(input_image, lower_threshold, upper_threshold):
    """
    Apply the Canny edge detection algorithm to an image using the given threshold values.
    
    :param input_image: The input image as a NumPy array.
    :param lower_threshold: The lower threshold for edges.
    :param upper_threshold: The upper threshold for edges.
    :return: The image with detected edges as a NumPy array.
    """
    return cv2.Canny(input_image, lower_threshold, upper_threshold)


def adjust_contrast_brightness(input_image, contrast, brightness):
    """
    Adjust the contrast and brightness of an image using the given factors.
    
    :param input_image: The input image as a NumPy array.
    :param contrast: The contrast adjustment factor.
    :param brightness: The brightness adjustment factor.
    :return: The image with adjusted contrast and brightness as a NumPy array.
    """
    return cv2.addWeighted(input_image, contrast, np.zeros(input_image.shape, input_image.dtype), 0, brightness)


def apply_operation(operation, image, **kwargs):
    """
    Apply the specified image processing operation to the input image.
    :param operation: The image processing operation to apply (from the ImageOperation enum).
    :param image: The input image as a NumPy array.
    :param kwargs: Additional keyword arguments for specific operations.
    :return: The processed image as a NumPy array, or None if the operation is not supported.
    """
    if operation == ImageOperation.HISTOGRAM_EQUALIZATION:
        return histogram_equalization(image)
    elif operation == ImageOperation.FILTER:
        return filter_image(image, kwargs['kernel'])
    elif operation == ImageOperation.THRESHOLD:
        return threshold_image(image, kwargs['threshold_value'])
    elif operation == ImageOperation.EROSION:
        return erosion_image(image, kwargs['kernel_size'], kwargs['iterations'])
    elif operation == ImageOperation.DILATION:
        return dilation_image(image, kwargs['kernel_size'], kwargs['iterations'])
    elif operation == ImageOperation.RESIZE:
        return resize_image(image, 2.0, 2.0)
    elif operation == ImageOperation.ROTATE:
        return rotate_image(image, 45)
    elif operation == ImageOperation.BLUR:
        return blur_image(image, 5)
    elif operation == ImageOperation.CANNY:
        return canny_image(image, 100, 200)
    elif operation == ImageOperation.CONTRAST_BRIGHTNESS:
        return adjust_contrast_brightness(image, 1.5, 50)
    else:
        return None


def process_image(input_image_path, output_dir, operations):
    """
    Process the input image using the specified operations and save the results to the output directory.
    :param input_image_path: The path to the input image.
    :param output_dir: The path to the output directory.
    :param operations: The list of image processing operations to apply (from the ImageOperation enum).
    """
    input_image = cv2.imread(input_image_path)

    if input_image is None:
        print(f"Error: Could not open the image file: {input_image_path}")
        return

    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for operation in operations:
            kwargs = {}  # Add any operation-specific arguments here
            future = executor.submit(apply_operation, operation, input_image, **kwargs)
            futures.append((future, operation))

        for future, operation in futures:
            result = future.result()
            cv2.imwrite(os.path.join(output_dir, f"{operation.name.lower()}_image.jpg"), result)

    print(f"Image processing completed successfully for: {input_image_path}")


def process_images(images, output_dir, operations):
    """
    Process multiple input images concurrently using the specified operations and save the results to the output directory.
    :param images: A list of paths to the input images.
    :param output_dir: The path to the output directory.
    :param operations: The list of image processing operations to apply (from the ImageOperation enum).
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_image, image, output_dir, operations) for image in images]
        concurrent.futures.wait(futures)

    print("All image processing tasks completed successfully.")


def main():
    """
    The main entry point of the script.
    Parses command-line arguments, processes the input images with the specified operations, and saves the results to the output directory.
    """
    parser = argparse.ArgumentParser(description="Multithreaded image processing in Python.")
    parser.add_argument("inputs", nargs="+", help="Paths to the input images.")
    parser.add_argument("output", help="Path to the output directory.")
    parser.add_argument(
        "-o",
        "--operations",
        nargs="+",
        choices=[operation.name.lower() for operation in ImageOperation],
        help="List of image processing operations to apply. Supported operations: resize, rotate, blur, canny, contrast_brightness, histogram_equalization, filter, threshold, erosion, dilation",
    )

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    operations = [ImageOperation[operation.upper()] for operation in args.operations]

    process_images(args.inputs, args.output, operations)


if __name__ == "__main__":
    main()

