from PIL import Image
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create a list to store all the data for saving to Excel
data_to_save = []

# Get all `.jpg` files dynamically from the current working directory
image_directory = f"{os.curdir}/Task3/task3Images/"
image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]
image_files.sort(key=lambda x: int(os.path.splitext(x.replace('.jpg', ''))[0]))

# Iterate through each image file
for file_name in image_files:
    try:
        file = os.path.join(image_directory, file_name)
        img = Image.open(file).convert('L')
        width, height = img.size
        
        right_half = img.crop((width // 2, 0, width, height - 8)).rotate(-90)
        width, height = right_half.size
        # right_half.save(f'd_{file_name}')
        
        img_np = np.array(right_half)
        min_color_val = np.min(img_np[img_np >= 30]) if np.any(img_np >= 30) else 255

        thumb_end = int(width * .40)
        remaining_width = width - thumb_end
        finger_width = remaining_width // 4
        
        finger_section = {
            "Thumb": (0, height - 56, thumb_end, height - 24),
            "Index": (thumb_end, 0, thumb_end + finger_width, height // 2),
            "Middle": (int(thumb_end + finger_width), 0, int(thumb_end + 2 * finger_width), height // 2),
            "Ring": (int(thumb_end + 2 * finger_width), 0, int(thumb_end + 3 * finger_width), height // 2),
            "Pinky": (int(thumb_end + 3 * finger_width), 0, int(thumb_end + 4 * finger_width), height // 2),
        }

        fingers = {finger: right_half.crop(box) for finger, box in finger_section.items()}
        
        # Store the finger pressures for this image
        finger_pressure = {}
        for finger, cropped_img in fingers.items():
            # Calculate the pressure based on the mean and std deviation
            x = (np.mean(np.array(cropped_img)) + np.std(np.array(cropped_img))) / 2
            finger_pressure[finger] = 1 if x >= min_color_val else 0

        # Save the results to the data_to_save list
        data_to_save.append({
            "Image": file_name.replace('.jpg', ''),
            "Thumb": finger_pressure["Thumb"],
            "Index": finger_pressure["Index"],
            "Middle": finger_pressure["Middle"],
            "Ring": finger_pressure["Ring"],
            "Pinky": finger_pressure["Pinky"]
        })

        print(f'{file_name}: {finger_pressure}\n')

        ## Visualize the cropped finger images stored in 'fingers' dictionary
        # fig, axes = plt.subplots(1, len(fingers), figsize=(15, 5))
        # for i, (finger, cropped_img) in enumerate(fingers.items()):
        #     axes[i].imshow(cropped_img, cmap="gray")  # Display grayscale image
        #     axes[i].set_title(f"{finger}-{finger_pressure[finger]}")  # Set title as finger name
        #     axes[i].axis("off")  # Hide axis labels

        # plt.tight_layout()
        # plt.show()

    except Exception as e:
        raise RuntimeError(f'Error processing {file_name}: {e}')
    finally:
        right_half.close()
        img.close()

# Create a DataFrame from the collected data
df = pd.DataFrame(data_to_save)

# Save the DataFrame to an Excel file
output_file = f"{os.curdir}/Task3/finger_pressures.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been saved to '{output_file}'.")
