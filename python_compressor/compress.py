import numpy as np
from scipy.fftpack import dct, idct
from skimage import io, color
import heapq
from collections import defaultdict, Counter
from huffman import huffman_compress_binary
from binary import save_to_file


# def generate_quant_matrix(q):
#     Q = np.array([
#         [16, 11, 10, 16, 24, 40, 51, 61],
#         [12, 12, 14, 19, 26, 58, 60, 55],
#         [14, 13, 16, 24, 40, 57, 69, 56],
#         [14, 17, 22, 29, 51, 87, 80, 62],
#         [18, 22, 37, 56, 68, 109, 103, 77],
#         [24, 35, 55, 64, 81, 104, 113, 92],
#         [49, 64, 78, 87, 103, 121, 120, 101],
#         [72, 92, 95, 98, 112, 100, 103, 99]
#     ])
#     return Q * (50/q)


def pad_to_multiple_of_8(matrix):
    # Get the current height and width of the matrix
    H, W = matrix.shape
    
    # Calculate how much padding is needed
    pad_h = (8 - H % 8) % 8  # Padding for height to make it a multiple of 8
    pad_w = (8 - W % 8) % 8  # Padding for width to make it a multiple of 8
    # print(pad_h, pad_w)
    
    # Apply the padding using numpy's pad function
    padded_matrix = np.pad(matrix, ((0, pad_h), (0, pad_w)), mode='constant', constant_values=0)
    
    return padded_matrix

def apply_dct_quantization(block, Q):
    # Step 1: Apply DCT (Discrete Cosine Transform)
    dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
    
    # Step 2: Quantization (element-wise division and rounding)
    quantized_block = np.round(dct_block / Q)
    
    return quantized_block

def zigzag_order(block):
    """
    Convert an 8x8 block into a 1D array in zigzag order.
    """
    zigzag_indices = [
        (0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (0, 2), (0, 3), (1, 2),
        (2, 1), (3, 0), (4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (0, 5),
        (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (6, 0), (5, 1), (4, 2),
        (3, 3), (2, 4), (1, 5), (0, 6), (0, 7), (1, 6), (2, 5), (3, 4),
        (4, 3), (5, 2), (6, 1), (7, 0), (7, 1), (6, 2), (5, 3), (4, 4),
        (3, 5), (2, 6), (1, 7), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3),
        (7, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7), (4, 7), (5, 6),
        (6, 5), (7, 4), (7, 5), (6, 6), (5, 7), (6, 7), (7, 6), (7, 7)
    ]
    return np.array([block[i, j] for i, j in zigzag_indices])

def replace_trailing_zeros_with_marker(block, marker=32767):
    """
    Replace trailing zeros with a marker value (default: 32767).
    """
    block = np.array(block)  # Ensure it's an array for indexing
    # Find the last non-zero position
    last_nonzero = np.max(np.where(block != 0)) if np.any(block != 0) else -1
    
    # Replace trailing zeros with the marker
    if last_nonzero == -1:
        result = [marker]  # Entire block is zero, only the marker should be added
    else:
        result = np.concatenate((block[:last_nonzero + 1], [marker]))
    
    return result


def flatten_and_compress_blocks(blocks, marker=32767):
    compressed_data = []
    for block in blocks:
        # Replace trailing zeros with the marker
        compressed_block = replace_trailing_zeros_with_marker(block, marker)
        # Append the compressed block to the final list
        compressed_data.extend(map(int, compressed_block))
    return compressed_data

def compress(filename, Q):
    img_name = filename.split(".")[0]
    image = io.imread(filename)
    # print(image[20][102])
    # image -= 128
    # print(image[20][102])
    shape = image.shape
    if(len(shape) == 3):
        print("color")
        compress_color(image, Q, img_name)
    elif(len(shape) == 2):
        print("greyscale")
        compress_greyscale(image, Q, "grey", img_name)
    else:
        print("Invalid image dimensions, not greyscale or color")


###############################################################################################################

def compress_greyscale(image, Q, colour, img_name):
    image = pad_to_multiple_of_8(image)
    # we are doing this cuz image might not have size as multiple of 8 na
    H = image.shape[0]
    W = image.shape[1]
    # print(H*W/64)
    blocks = image.reshape(H // 8, 8, W // 8, 8)
    
    # divide it into blocks
    
    # Rearrange the axes to get a list of blocks
    blocks = blocks.swapaxes(1, 2).reshape(-1, 8, 8)
    
    # quantized_blocks = np.apply_along_axis(apply_dct_quantization, axis=1, arr=blocks, Q=Q)
    # print(blocks[2000])
    quantized_blocks = np.array([apply_dct_quantization(block, Q) for block in blocks])
    # print(quantized_blocks.shape)
    # print(quantized_blocks[2000])
    
    # now hard part starts

    # first we need to do zigzag ordering
    zigzagged_blocks = np.array([zigzag_order(block) for block in quantized_blocks])
    # print(zigzagged_blocks.shape)
    

    # next we need to do replace trailing zero's with a EOB marker
    # now concatenate all these compressed blocks
    compressed_blocks = np.array(flatten_and_compress_blocks(zigzagged_blocks))
    # print(compressed_blocks[-1])
    print(compressed_blocks.shape, "->", colour)

    # next we will have to implement huffman encoding
    # and we need to create a bit string which we need to save in some file
    huffman_encoded_bit_string = huffman_compress_binary(compressed_blocks)

    # Calculate H/8 and W/8
    H_div_8 = H // 8  
    W_div_8 = W // 8 

    # Convert them to strings of size 10
    H_str = format(H_div_8, '010b')  
    W_str = format(W_div_8, '010b')

    # Combine the two strings into a single 20-bit string
    size_str = H_str + W_str
    final_bit_string = '0' + size_str + huffman_encoded_bit_string # greyscale hence 0
    # print(final_bit_string[:100])

    # filename = filename[:-4] + '.bin' # remove the '.png' or '.jpg' part and put '.bin'
    img_name += '_' + colour + '.bin'
    save_to_file(final_bit_string, img_name)
    return

def compress_color(image, Q, img_name):
    red_img, green_img, blue_img = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    compress_greyscale(red_img, Q, "red", img_name)
    compress_greyscale(green_img, Q, "green", img_name)
    compress_greyscale(blue_img, Q, "blue", img_name)
    return


