# Real-Time Object Detection with CLIP and OpenCV

This project uses OpenAI's CLIP model and OpenCV to perform real-time object detection using a webcam. The model identifies objects from a predefined list of queries and draws bounding boxes around them.

## Installation

1. **Clone the repository:**
  
    git clone https://github.com/yourusername/repo-name.git
    cd repo-name
  

2. **Install the required packages:**
    
    pip install numpy pandas opencv-python torch torchvision transformers matplotlib
    

3. **Download the CLIP model:**
    The CLIP model will be automatically downloaded the first time you run the code.

## Usage

1. **Run the script:**
    
    python CV_Project.py
  

2. **Interact with the webcam:**
    - The webcam feed will be displayed in a window.
    - Press `q` to quit the application.

## Code Overview

- **Imports and setup:**
    - Import necessary libraries and set up the CLIP model and processor.
    - Define the device (CPU or CUDA) for running the model.

- **Main loop:**
    - Capture frames from the webcam.
    - Process each frame and break it into patches.
    - Compute similarity scores between patches and query texts.
    - Draw bounding boxes around detected objects.


