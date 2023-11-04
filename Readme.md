# DICOM File Processing Project

### This project is designed for working with medical data in the DICOM format. It includes scripts and utilities that provide data conversion, sorting, and analysis, as well as the creation and training of a classifier to determine the modality and body parts depicted in the images.

## Description of the Original Model

- Supports .jpg images with three RGB channels and the following modalities and body parts: CT of the head, abdominal cavity, and chest; X-ray of the wrist, abdominal cavity, and chest.
- However, you can train the model based on your own data, and all tools (except for creating a .csv file with data and attributes) are provided in the application.

## Project Structure

+ requirements.txt: A text file containing all the Python libraries required for the project.
+ Dockerfile: Docker image settings.
+ app/: Directory containing scripts and processed data.
   + checkpoints: Folder with saved model checkpoints.
   + logs: Model logs and journals.
   + classifier.py: Script for image classification based on the trained model.
   + api.py: API handler.
   + bin/: Directory with main data processing scripts.
      + dicom_refactor.py: Script for converting DICOM files to .jpg images.
      + sort.py: Script for sorting DICOM files by modality and body parts based on metadata.
      + classifier/: Root directory of the model.
         + dataset.py: Script for reading attributes from .csv files and creating datasets.
         + jpg_rgb_refactor.py: Script for converting images to .jpg format with three RGB channels (you can choose one or both options).
         + model.py: Script containing the classifier model configuration.
         + model_test.py: Script for model testing.
         + split_data.py: Script for creating train.csv and val.csv from the .csv file with file names and attributes for training.
         + train.py: Main script responsible for training the model.
         + train.csv: File created by split_data.py, containing paths and attributes of random 80% of the original images for training.
         + val.csv: File created by split_data.py, containing paths and attributes of the remaining 20% of the original images for training.

## Manual Training Instructions (via Terminal)

1. Sorting DICOM Files: If you want to sort DICOM files by metadata (e.g., Modality or BodyPartExamined), you can use sort.py. It sorts files into corresponding subdirectories within the initial directory. Run it as follows:
```python sort.py [path to the initial directory] [y or n]```
   - y: Sorts all files by modality and body parts.
   - n: Sorts files by modality only.

2. Preprocessing DICOM Files: To preprocess DICOM files, you can use dicom_refactor.py. It converts DICOM files to JPEG images and saves them in the /img subdirectory. Run it as follows:
```python dicom_refactor.py [path to the directory with DICOM files]```

3. Converting Images to RGB: If you want to convert images to RGB format, you can use jpg_rgb_refactor.py. It performs this operation and saves the updated files in the same directory. You can run it as follows:
```python jpg_rgb_refactor.py [path to the image directory] [0 or 1 or 2]```
   - 0: Convert to JPEG format only.
   - 1: Convert to RGB format only.
   - 2: Both steps (JPEG and RGB).

4. Data Preparation for Model Training: Before starting model training for image modality and body part recognition, you should split the data into training and testing using split_data.py. This script creates train.csv and val.csv files containing image names, modality, and body parts. However, this information is taken from a user-created .csv file with labels. You can run it as follows:
```python split_data.py [path to the initial image directory] [path to the working directory where train.csv and val.csv files will be saved] [path to the .csv file containing image information]```

5. Model Training: If you have prepared everything necessary for model training, use train.py. This script uses all the data you have prepared to train the image classifier. You can run it as follows:
```python split_data.py [path to the image directory] [path to train.py] [path where model checkpoints will be saved after training] [use the CPU for training - "cpu," use the GPU for training - "cuda"] [number of training epochs (more epochs = longer training time and increased accuracy)] [number of images loaded into memory at once (smaller batch size = longer training time and increased accuracy)] [number of processes generating batches in parallel (more parallel processes = less training time and higher CPU load)]```

## Environment Recommendations

- Create a Python virtual environment to isolate project dependencies.
- Install all necessary libraries by running the command ```python3 -m pip install -r requirements.txt``` in the terminal.
- If you want to recreate the application build process (or modify it), you can run the following commands in the terminal:
   - ```python -m venv venv```
   - ```source venv/bin/activate``` (or ```venv\Scripts\activate``` for Windows)
   - ```pip install -r requirements.txt```

## Working with the Container and Post-Request

Download the Docker image:

```docker pull stilusoff/classifier-api:latest```

Run the Docker container:

```docker run -p [local machine port]:[container port for redirection] -e HOST=[host the container will listen on] -e PORT=[port where the API inside the container will be running] stilusoff/classifier-api```

Request parameters: image, archive

Examples of requests:

```curl -X POST -F "image=@c:\Python_Projects\test\2_0_40.jpg" http://localhost:5000/classify```

```curl -X POST -F "archive=@c:\Python_Projects\test\test.rar" http://localhost:5000/classify```

## Requirements

- Python 3.9.xx and higher
- Python libraries listed in requirements.txt
- If model training does not use CUDA, but your system configuration meets the requirements, it is recommended to use the command ```pip install torch==1.7.0 -f https://download.pytorch.org/whl/torch_stable.html```
