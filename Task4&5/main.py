import torch
from PIL import Image
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import os

# Get all `.jpg` files dynamically from the current working directory
image_directory = f"{os.curdir}/Task4&5/Chess_dataset/"
image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]
image_files.sort(key=lambda x: int(os.path.splitext(x
                                                    .replace('.jpg', '')
                                                    .replace('(', '')
                                                    .replace(')', ''))[0]))

# Load the YOLOv5 model
print('Loading model...')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
print('model loaded.')

# Define the transformation for the input image
transform = transforms.Compose([
    transforms.Resize((640, 640)),
    transforms.ToTensor()
])

for img in image_files:
    # Load and transform the image
    print('Loading img...')
    img = Image.open(img).convert('RGB')
    img_transformed = transform(img).unsqueeze(0)
    print('img loaded.')
    
    print('Performing inference...')
    # Perform inference
    results = model(img_transformed)
    print('Inference performed.')

    # Print results
    results.print()

    # Render results
    results.render()
    
    print(f"results type: {type(results)}")
    print(f"img type: {type(img)}")
    print(f"img_transformed type: {type(img_transformed)}")

    # Display the image with bounding boxes
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
