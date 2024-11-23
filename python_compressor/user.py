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
    return np.round(Q * (50/q))

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
    # image_path = "ISKCON_Durban.jpg"  # Replace with your image path
    image_path = input("Enter image name: ")  # Set the image path
    img_name = image_path.split(".")[0]

    quality_factor = int(input("Enter compression value (integer in range [1-100]) : "))  # Set the quality factor (can be adjusted)
    quant_matrix = generate_quant_matrix(quality_factor)

    img = io.imread(image_path)
    shape = img.shape
    print("shape is:", shape)

    compressed_img = f"{img_name}_compressed.jpg"

    compress(image_path, quant_matrix)

    if(len(shape) == 3):
        red_bin = f"{img_name}_red.bin"
        green_bin = f"{img_name}_green.bin"
        blue_bin = f"{img_name}_blue.bin"
        
        red_decoded = decompress(red_bin, quant_matrix, img_name, color="red")
        green_decoded = decompress(green_bin, quant_matrix, img_name, color="green")
        blue_decoded = decompress(blue_bin, quant_matrix, img_name, color="blue")

        I1 = io.imread(f"{img_name}_red_compressed.jpg")
        I2 = io.imread(f"{img_name}_green_compressed.jpg")
        I3 = io.imread(f"{img_name}_blue_compressed.jpg")
        I1 = I1.astype(np.uint8)
        I2 = I2.astype(np.uint8)
        I3 = I3.astype(np.uint8)
        reconstructed_image = np.stack((I1, I2, I3), axis=-1)

        io.imsave(compressed_img, reconstructed_image) 
        print(calculate_rmse(img, reconstructed_image))

    elif(len(shape) == 2):
        binary_path = f"{img_name}_grey.bin"
        decompress(binary_path, quant_matrix, img_name, color="grey")
        
        image1 = io.imread(image_path)
        image2 = io.imread(f"{img_name}_grey_reconstruct.jpg")
        # image2 = io.imread("compressed.jpg")

        print(calculate_rmse(image1, image2))



