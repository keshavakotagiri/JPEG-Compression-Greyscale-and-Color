% Read the grayscale image
img = imread('kodak24.png'); % replace with your image path
% img = rgb2gray(img); % convert to grayscale if needed
img = double(img);

% Define block size and JPEG quantization matrix
blockSize = 8;
Q = [16 11 10 16 24 40 51 61;
     12 12 14 19 26 58 60 55;
     14 13 16 24 40 57 69 56;
     14 17 22 29 51 87 80 62;
     18 22 37 56 68 109 103 77;
     24 35 55 64 81 104 113 92;
     49 64 78 87 103 121 120 101;
     72 92 95 98 112 100 103 99];

% Get image dimensions and initialize compressed image
[rows, cols] = size(img);
compressedImg = zeros(size(img));

% Loop over 8x8 blocks
for i = 1:blockSize:rows
    for j = 1:blockSize:cols
        % Extract 8x8 block
        block = img(i:i+blockSize-1, j:j+blockSize-1);

        % Apply DCT
        dctBlock = dct2(block);

        % Quantize
        quantizedBlock = round(dctBlock ./ Q);

        % Dequantize
        dequantizedBlock = quantizedBlock .* Q;

        % Apply inverse DCT
        compressedBlock = idct2(dequantizedBlock);

        % Store compressed block
        compressedImg(i:i+blockSize-1, j:j+blockSize-1) = compressedBlock;
    end
end

% Convert to uint8 and display
compressedImg = uint8(compressedImg);

outputBaseFileName = 'E:/IIT Bombay/4th_yr/CS 663 - Fundamentals of Digital Image Processing/Project/compressed.jpg';
imwrite(compressedImg, outputBaseFileName);
imshow(compressedImg);
