from compress import compress
from decompress import decompress
import numpy as np
from skimage import io, color

def generate_quant_matrix(q):
    Q = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ])
    return Q * (50/q)

def calculate_rmse(image1, image2):
    # Ensure the images are numpy arrays
    image1 = np.array(image1)
    image2 = np.array(image2)

    # Check if the images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Images must have the same dimensions")

    # Calculate the squared differences between the images
    squared_diff = (image1 - image2) ** 2

    # Calculate the MSE
    mse = np.mean(squared_diff)
    rmse = np.sqrt(mse)
    
    return rmse


if __name__ == "__main__":
    quality_factor = 50  # Set the quality factor (can be adjusted)
    quant_matrix = generate_quant_matrix(quality_factor)
    # image_path = "ISKCON_Durban.jpg"  # Replace with your image path
    image_path = "kodak24.jpg"
    compress(image_path, quant_matrix)
    binary_path = "kodak24.bin"
    decompress(binary_path, quant_matrix)

    image1 = io.imread(image_path)
    image2 = io.imread(image_path[:-4] + "_reconstruct.jpg")
    # image2 = io.imread("compressed.jpg")

    print(calculate_rmse(image1, image2))

