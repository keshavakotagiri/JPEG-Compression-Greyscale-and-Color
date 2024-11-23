import numpy as np

# luminance quantization table :
qY = np.array([[16, 11, 10, 16, 24, 40, 51, 61],  
                [12, 12, 14, 19, 26, 48, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]])

# chrominance quantization table :
qC = np.array([[17, 18, 24, 47, 99, 99, 99, 99],  
                [18, 21, 26, 66, 99, 99, 99, 99],
                [24, 26, 56, 99, 99, 99, 99, 99],
                [47, 66, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99]])

# convert RGB image to grayscale image(lUMINANCE)
def rgb_to_gray(img):
  red, green, blue = img[:,:,0], img[:,:,1], img[:,:,2]
  # Formula of the Luminance
  return 0.299*red + 0.587*green + 0.114*blue

# convert RGB image to YCbCr image
def rgb_to_ycbcr(img):
    ycbcr_image = img.copy()
    red, green, blue = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    
    ycbcr_image[:, :, 0] = 0.299 * red + 0.587 * green + 0.114 * blue
    ycbcr_image[:, :, 1] = 128 - 0.168736 * red - 0.331264 * green + 0.5 * blue
    ycbcr_image[:, :, 2] = 128 + 0.5 * red - 0.418688 * green - 0.081312 * blue

    return ycbcr_image

# convert YCbCr image to RGB image
def ycbcr_to_rgb(img):
    rgb_image = img.copy()                                    
    y, cb, cr = img[:,:,0], img[:,:,1], img[:,:,2]
    rgb_image[:,:,0] = y + 1.14020*(cr-128)                       
    rgb_image[:,:,1] = y - 0.34414*(cb-128) - 0.71414*(cr-128)   
    rgb_image[:,:,2] = y + 1.77200*(cb-128)                     
    return rgb_image