Concurrent Image Processing Toolbox

Overview
The Concurrent Image Processing Toolbox is a Python-based application designed to perform various image processing operations on multiple images concurrently. The project utilizes the OpenCV library for image processing tasks and Python's built-in threading capabilities for concurrent execution.


Usage Instructions

To use the Concurrent Image Processing Toolbox, follow these steps:

Install the required dependencies:
pip install opencv-python
pip install opencv-python-headless

Clone the repository or download the source files.
Modify the concurrent_image_processing.py script to include the desired image processing operations and input/output paths.

Run the script:
(Path of images, path of output folder, and list of operations to execute)

python concurrent_image_processing.py input1.jpg input2.png input3.bmp -o output_dir -o resize rotate blur histogram_equalization filter threshold erosion dilation

OR

(if you've made the necessary changes in the concurrent_image_processing.py file already)
python concurrent_image_processing.py


Design Decisions:


OpenCV library: We chose the OpenCV library for its extensive support for image processing operations and its efficiency in handling large images. OpenCV also provides good compatibility with NumPy, allowing for easy manipulation of image data.

Threading: To achieve concurrency, Python's built-in threading module was used to create and manage threads. We implemented a thread-safe queue to store image processing tasks and distribute them among available worker threads.

Modular design: The code is organized into modular functions and classes, making it easy to extend with new image processing operations or modify existing ones.

Error handling: Input validation and error handling were added to ensure the robustness of the application, especially when processing a large number of images with varying sizes and formats.


Known Limitations


Global Interpreter Lock (GIL): The Python Global Interpreter Lock (GIL) can limit the performance benefits of multithreading in some cases, as it allows only one thread to execute Python bytecode at a time. This limitation might affect the speedup achieved through concurrency, especially when using CPU-bound operations. However, the impact on this specific project is limited due to the reliance on OpenCV, which releases the GIL during execution of its functions.

Supported image formats: Currently, the toolbox supports only the image formats that OpenCV can read and write (e.g., JPEG, PNG, BMP). 

Advanced thread management: The current implementation uses a simple thread pool and a thread-safe queue for task distribution. More advanced thread management techniques, such as dynamic thread creation or load balancing could be implemented.

GUI: The toolbox currently lacks a graphical user interface (GUI), which might make it less user-friendly for non-programmers. Adding a GUI would improve its usability and make it more accessible to a wider audience.


Benchmarking Results:

The speedup achieved through concurrency depends on several factors, including the number of CPU cores available, the number of images being processed, the types of operations being performed, and the size of the images.

In our system, when we compared the execution time of operations with and without concurrency, it was found that the multi-threaded version was ~80% faster than the single thread image augmentation task.
