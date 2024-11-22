import numpy as np
from scipy.fftpack import dct, idct
from skimage import io, color
import heapq
from collections import defaultdict, Counter
from huffman import huffman_decompress_binary
from binary import load_from_file

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


def decompress_blocks(compressed_data, block_size=64, marker=32767):
    blocks = []
    current_block = []
    
    for num in compressed_data:
        if num == marker:  # When the EOB marker is found
            # Ensure the block size is 64
            remaining_zeros = block_size - len(current_block)
            current_block.extend([0] * remaining_zeros)  # Add trailing zeros back
            blocks.append(np.array(current_block))  # Add the block to the list
            current_block = []  # Reset for the next block
        else:
            current_block.append(num)  # Add the number to the current block
        
        # If we reach 64 elements without seeing the EOB (this should not usually happen)
        if len(current_block) == block_size:
            blocks.append(np.array(current_block))  # Add the full block to the list
            current_block = []  # Reset for the next block
    
    return blocks

def convert_to_8x8(block):
    # Reshape the block (a 1D array with 64 elements) into a 2D array (8x8)
    return np.reshape(block, (8, 8))

def apply_idct_dequantize(block, Q):
    block_dequantized = block * Q
    # Apply IDCT to each row
    block_idct_rows = idct(block_dequantized, axis=1, norm='ortho')
    # Apply IDCT to each column of the result
    block_idct_dequantized = idct(block_idct_rows, axis=0, norm='ortho')
    return block_idct_dequantized

def rejoin_blocks(blocks, num_H_blocks, num_W_blocks):
    # Create an empty array to hold the reconstructed image (size H x W)
    reconstructed_image = np.zeros((num_H_blocks * 8, num_W_blocks * 8))
    
    # Iterate through the blocks and place them in the appropriate location
    block_index = 0
    for i in range(num_H_blocks):
        for j in range(num_W_blocks):
            # Place each block in the correct position in the reconstructed image
            reconstructed_image[i*8:(i+1)*8, j*8:(j+1)*8] = blocks[block_index]
            block_index += 1
    
    return reconstructed_image


def decompress(filename, Q):
    encoded_data = load_from_file(filename)
    # print(encoded_data[:100])
    # print(f"encoded_data[:10]: {encoded_data[:10]}")
    grey_or_col = encoded_data[0]
    encoded_data = encoded_data[1:]
    # print(type(grey_or_col))
    if(grey_or_col == '0'):
        print("greyscale_decompress", grey_or_col)
        num_H_blocks = int(encoded_data[:10], 2)
        encoded_data = encoded_data[10:]
        num_W_blocks = int(encoded_data[:10], 2)
        encoded_data = encoded_data[10:]
        decompress_greyscale(encoded_data, Q, filename, num_H_blocks, num_W_blocks)
    else:
        print("color_decompress", grey_or_col)
        num_H_blocks = int(encoded_data[:10], 2)
        encoded_data = encoded_data[10:]
        num_W_blocks = int(encoded_data[:10], 2)
        encoded_data = encoded_data[10:]
        decompress_color(encoded_data, Q, filename, num_H_blocks, num_W_blocks)
    return

###############################################################################################################

def decompress_greyscale(encoded_data, Q, filename, num_H_blocks, num_W_blocks):
    arr = np.array(huffman_decompress_binary(encoded_data))
    blocks = decompress_blocks(arr)
    blocks = np.array(blocks)
    reshaped_blocks = [convert_to_8x8(block) for block in blocks]
    idct_dequantize_blocks = [apply_idct_dequantize(block, Q) for block in reshaped_blocks]  # Apply dequantize to each block and then IDCT
    
    reconstructed_image = rejoin_blocks(idct_dequantize_blocks, num_H_blocks, num_W_blocks)

    image_to_save = np.clip(reconstructed_image, 0, 255).astype(np.uint8)  # Clip values to range 0-255 and convert to uint8
    
    # Save the image using skimage.io.imsave
    filename = filename[:-4] + "_reconstruct.jpg" # remove the .bin at the end and add .jpg
    io.imsave(filename, image_to_save)
    return

def decompress_color(encoded_data, Q, filename, num_H_blocks, num_W_blocks):
    return