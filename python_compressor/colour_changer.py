import numpy as np
from skimage import io, color
from skimage.transform import resize
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
    # Ensure img is a floating-point array for precision
    img = img.astype(np.float32)
    y, cb, cr = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    # Apply the YCbCr to RGB conversion formulas
    r = y + 1.402 * (cr - 128)
    g = y - 0.344136 * (cb - 128) - 0.714136 * (cr - 128)
    b = y + 1.772 * (cb - 128)

    # Stack and clip to ensure valid RGB values
    rgb_image = np.stack((r, g, b), axis=-1)
    rgb_image = np.clip(rgb_image, 0, 255).astype(np.uint8)
    return rgb_image


def downsample_channel(channel, factor=2):
    downsampled = resize(channel, (channel.shape[0] // factor, channel.shape[1] // factor), anti_aliasing=True)
    downsampled = (downsampled * 255).astype(np.uint8)
    return downsampled

def upsample_channel(channel, original_shape):
    upsampled = resize(channel, original_shape, anti_aliasing=True)
    upsampled = (upsampled * 255).astype(np.uint8)
    return upsampled