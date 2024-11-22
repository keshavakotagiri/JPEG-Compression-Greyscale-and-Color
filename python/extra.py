from skimage import io, color
import numpy as np

l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
l *= 8
l = [l]
l *= 80

l = np.array(l)
print(l.shape)
H = l.shape[0]
W = l.shape[1]
blocks = l.reshape(H // 8, 8, W // 8, 8)
blocks = blocks.swapaxes(1, 2).reshape(-1, 8, 8)

print(blocks.shape)
