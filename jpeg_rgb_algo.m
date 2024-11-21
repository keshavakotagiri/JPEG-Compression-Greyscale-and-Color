function compressed_image = compressRGB(img, blockSize, Q, compression_ratio)
    img = double(img);
    [rows, cols, channels] = size(img);

    % Add padding to each channel to ensure dimensions are multiples of blockSize
    padded_rows = ceil(rows / blockSize) * blockSize;
    padded_cols = ceil(cols / blockSize) * blockSize;
    img_padded = zeros(padded_rows, padded_cols, channels);
  
    for ch = 1:channels
        img_padded(:, :, ch) = padarray(img(:, :, ch), ...
            [padded_rows - rows, padded_cols - cols], 'post');
    end

    % Scale the quantization matrix based on the compression ratio
    scaled_Q = Q * (100 / compression_ratio);

    % Initialize compressed image
    compressed_img = zeros(size(img_padded));

    % Process each channel independently
    for ch = 1:channels
        channel = img_padded(:, :, ch);
        for i = 1:blockSize:size(channel, 1)
            for j = 1:blockSize:size(channel, 2)
                % Extract block
                block = channel(i:i+blockSize-1, j:j+blockSize-1);

                % Apply DCT, Quantization, Dequantization, and IDCT
                dctBlock = dct2(block);
                quantizedBlock = round(dctBlock ./ scaled_Q);
                dequantizedBlock = quantizedBlock .* scaled_Q;
                compressedBlock = idct2(dequantizedBlock);

                % Store compressed block
                compressed_img(i:i+blockSize-1, j:j+blockSize-1, ch) = compressedBlock;
            end
        end
    end

    % Clip values to valid range and convert back to uint8
    compressed_image = uint8(max(min(compressed_img(1:rows, 1:cols, :), 255), 0));
end

% Main script
img_name = input('Enter the image name: ', 's');
compression_ratio = input('Enter the compression percentage (1-100): ');

img = imread(img_name);
if size(img, 3) ~= 3
    error('Input image must be an RGB image.');
end

% Resize the image if it exceeds the maximum supported dimensions
max_dim = 65500;
if size(img, 1) > max_dim || size(img, 2) > max_dim
    scale_factor = max_dim / max(size(img));
    img = imresize(img, scale_factor);
end

blockSize = 8; % Define block size
Q = [16 11 10 16 24 40 51 61;
     12 12 14 19 26 58 60 55;
     14 13 16 24 40 57 69 56;
     14 17 22 29 51 87 80 62;
     18 22 37 56 68 109 103 77;
     24 35 55 64 81 104 113 92;
     49 64 78 87 103 121 120 101;
     72 92 95 98 112 100 103 99];

output_img = compressRGB(img, blockSize, Q, compression_ratio);
output_img_name = sprintf('compressed_%s_%dpercent.png', img_name, compression_ratio); % Save as PNG
imwrite(output_img, output_img_name);
% Display the original and compressed images side by side
figure;
subplot(1, 2, 1);
imshow(img);
title('Original Image');

subplot(1, 2, 2);
imshow(output_img);
title('Compressed Image');

% Calculate and display the Mean Squared Error (MSE)
mse_value = immse(img, output_img);
fprintf('Mean Squared Error (MSE): %.4f\n', mse_value);

