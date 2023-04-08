#Imports
import timeit
#import os
import cv2
from main import apply_operation, ImageOperation
def benchmark_apply_operation(operation, input_image, *args, **kwargs):
    """
    Benchmark the execution time of an image processing operation by applying
    the specified operation to the input_image using the given arguments and
    keyword arguments.

    :param operation: The image processing operation to be benchmarked.
    :type operation: ImageOperation
    :param input_image: The input image to be processed.
    :type input_image: numpy.ndarray
    :param args: Positional arguments for the image processing operation.
    :param kwargs: Keyword arguments for the image processing operation.
    :return: None
    """
    input_image = cv2.imread('test_image.jpg', cv2.IMREAD_COLOR)
    assert input_image is not None, "Test image not found."

    operations = [ImageOperation.RESIZE, ImageOperation.ROTATE, ImageOperation.BLUR]

    for operation in operations:
        exec_time = timeit.timeit(
            'apply_operation(operation, input_image, **kwargs)',
            globals=globals(),
            number=100
        )
        print(f"{operation.name}: {exec_time:.4f} seconds")

if __name__ == '__main__':
    benchmark_apply_operation()