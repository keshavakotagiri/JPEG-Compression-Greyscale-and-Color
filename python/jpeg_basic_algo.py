import numpy as np
from scipy.fftpack import dct, idct
from skimage import io, color

# Read the grayscale image
img = io.imread('kodak24.jpg')  # replace with your image path
# Convert to grayscale if the image is in RGB
if img.ndim == 3:
    img = color.rgb2gray(img)
img = np.double(img)  # Convert to float for precision

# Define block size and JPEG quantization matrix
blockSize = 8
Q = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
              [12, 12, 14, 19, 26, 58, 60, 55],
              [14, 13, 16, 24, 40, 57, 69, 56],
              [14, 17, 22, 29, 51, 87, 80, 62],
              [18, 22, 37, 56, 68, 109, 103, 77],
              [24, 35, 55, 64, 81, 104, 113, 92],
              [49, 64, 78, 87, 103, 121, 120, 101],
              [72, 92, 95, 98, 112, 100, 103, 99]])

Q = Q * (50 /50)  # Adjust the quantization matrix

# Get image dimensions and initialize compressed image
rows, cols = img.shape
compressedImg = np.zeros_like(img)

# Loop over 8x8 blocks
for i in range(0, rows, blockSize):
    for j in range(0, cols, blockSize):
        # Extract 8x8 block
        block = img[i:i + blockSize, j:j + blockSize]

        # Apply DCT
        dctBlock = dct(dct(block.T, norm='ortho').T, norm='ortho')

        # Quantize
        quantizedBlock = np.round(dctBlock / Q)

        # Dequantize
        dequantizedBlock = quantizedBlock * Q

        # Apply inverse DCT
        compressedBlock = idct(idct(dequantizedBlock.T, norm='ortho').T, norm='ortho')

        # Store compressed block
        compressedImg[i:i + blockSize, j:j + blockSize] = compressedBlock

# Convert to uint8 and save the compressed image
compressedImg = np.uint8(np.clip(compressedImg, 0, 255))  # Clip values to [0, 255]
outputBaseFileName = 'compressed.jpg'
io.imsave(outputBaseFileName, compressedImg)

# Optionally display the image (if needed)
# io.imshow(compressedImg)
# io.show()
