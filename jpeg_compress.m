function jpeg_compress(filename, subsample_factor)
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

    % Step 1: Read the input image
    img = imread([filename '.jpg']);
    
    % Step 2: Check if the image is grayscale or color
    [H, W, numChannels] = size(img);
    
    % Apply subsampling only if the image is color
    if numChannels == 3
        % Convert RGB to YCbCr
        imgYCbCr = rgb2ycbcr(img);
        
        % Apply subsampling (e.g., 4:2:2, 4:4:4, etc.)
        [Y, Cb, Cr] = applySubsampling(imgYCbCr, subsample_factor, H, W);
        
        % Number of blocks for each channel (Y, Cb, Cr)
        numYBlocks = (H / 8) * (W / 8);
        numCbCrBlocks = (numYBlocks / subsample_factor(2)); % Use subsample_factor for Cb and Cr
        
        % Store Y, Cb, Cr blocks separately for encoding
        Y_blocks = breakIntoBlocks(Y, H, W);
        Cb_blocks = breakIntoBlocks(Cb, H, W);
        Cr_blocks = breakIntoBlocks(Cr, H, W);
        
        blocks = {Y_blocks, Cb_blocks, Cr_blocks};
    else
        % Grayscale image: no conversion needed
        blocks = {breakIntoBlocks(img, H, W)};
    end
    
    % Step 3: Perform DCT, quantization, and rounding for each block
    quantizedBlocks = cell(1, numel(blocks));
    
    for i = 1:numel(blocks)
        block = blocks{i};
        quantizedBlock = applyDCTQuantization(block, Q);
        quantizedBlocks{i} = quantizedBlock;
    end
    
    % Step 4: Create the binary bitstream
    bitStream = [];
    
    % First bit: 0 for grayscale, 1 for color
    bitStream = [bitStream, numChannels == 3];
    
    % Next 10 bits: Width (W/8) and Height (H/8)
    bitStream = [bitStream, dec2bin(W/8, 10), dec2bin(H/8, 10)];
    
    % Step 5: Encode each block using zigzag and Huffman encoding
    for i = 1:numel(quantizedBlocks)
        blockData = quantizedBlocks{i};
        
        % Zigzag ordering
        zigzagData = zigzagList(blockData);
        
        % Huffman encoding
        encodedBlock = huffmanEncode(zigzagData);
        
        % Concatenate the bitstream
        bitStream = [bitStream, encodedBlock];
    end
    
    % Step 6: Save the bitstream to a binary file
    saveBitString(bitStream, [filename, '.bin']);
end

% Helper functions
function blocks = breakIntoBlocks(img, H, W)
    % Break the image into 8x8 blocks
    blocks = mat2cell(img, repmat(8, 1, H/8), repmat(8, 1, W/8));
end

function [Y, Cb, Cr] = applySubsampling(imgYCbCr, subsample_factor, H, W)
    % Apply subsampling to Cb and Cr channels based on subsample_factor
    Y = imgYCbCr(:,:,1);
    Cb = imgYCbCr(:,:,2);
    Cr = imgYCbCr(:,:,3);
    
    % Apply subsampling for Y, Cb, and Cr based on subsample_factor
    if subsample_factor(2) == 2  % Example 4:2:2 subsampling for Cb and Cr
        Cb = Cb(1:2:end, 1:2:end);
        Cr = Cr(1:2:end, 1:2:end);
    elseif subsample_factor(2) == 1  % 4:4:4, no subsampling for Cb and Cr
        % Do nothing
    end
    
    % For Y (luminance), apply subsampling as per the factor
    if subsample_factor(1) == 2  % Example: 4:2:2, we subsample Y by 2 horizontally
        Y = Y(1:2:end, :);
    elseif subsample_factor(1) == 1  % No subsampling for Y (4:4:4)
        % Do nothing
    end
end

function quantizedBlock = applyDCTQuantization(block, Q)
    % Apply 2D DCT and quantization
    dctBlock = dct2(block);  % Apply 2D DCT
    quantizedBlock = round(dctBlock ./ Q);  % Quantization
end


function encodedBlock = huffmanEncode(data)
    % Perform Huffman encoding on the zigzag data (already implemented)
    encodedBlock = modifiedHuffmanEncode(data);
end


function saveBitString(bitString, filename)
    % Ensure the bit string length is a multiple of 8
    paddingLength = mod(-length(bitString), 8); % Find how many bits to pad
    bitString = [bitString, repmat('0', 1, paddingLength)]; % Pad with zeros if necessary

    % Convert bit string to numeric bytes
    byteArray = uint8(bin2dec(reshape(bitString, 8, []).')); % Group into bytes and convert to decimal

    % Save to a binary file
    fileID = fopen(filename, 'w'); % Open file for writing
    fwrite(fileID, byteArray, 'uint8'); % Write the byte array as binary
    fclose(fileID); % Close the file

    fprintf('Bit string saved to binary file: %s\n', filename);
end

