blockSize = 8;
Q = [16 11 10 16 24 40 51 61;
     12 12 14 19 26 58 60 55;
     14 13 16 24 40 57 69 56;
     14 17 22 29 51 87 80 62;
     18 22 37 56 68 109 103 77;
     24 35 55 64 81 104 113 92;
     49 64 78 87 103 121 120 101;
     72 92 95 98 112 100 103 99];

function decodeImageFromFile(filename)
    % Open the binary file for reading
    fid = fopen([filename '.bin'], 'rb');
    
    if fid == -1
        error('Failed to open file.');
    end
    
    % Step 1: Read the first bit to determine image type (grayscale or color)
    imgType = fread(fid, 1, 'ubit1'); % 0 for grayscale, 1 for color
    
    % Step 2: Read the number of blocks (W/8 and H/8) as 10-bit values
    W_blocks = fread(fid, 1, 'ubit10'); % Number of blocks in horizontal direction
    H_blocks = fread(fid, 1, 'ubit10'); % Number of blocks in vertical direction

    % Calculate the total number of blocks expected
    if imgType == 0
        expectedBlocks = (W_blocks * H_blocks); % For grayscale: W * H blocks
    else
        expectedBlocks = (W_blocks * H_blocks * 3); % For color: 3 channels
    end
    
    blocks = cell(1, expectedBlocks);
    blockIdx = 1;
    
    while true
        % Step 3: Read the 10-bit value to get the size of the Huffman table
        huffmanTableSize = fread(fid, 1, 'ubit10');
        
        % If we read zero here, we're at the end of the file (padding)
        if huffmanTableSize == 0
            break;
        end
        
        % Step 4: Read the Huffman table
        huffmanTable = readHuffmanTable(fid, huffmanTableSize); % Function to parse the Huffman table
        
        % Step 5: Decode the current block using the Huffman table
        blockData = decodeBlock(fid, huffmanTable); % Function to decode the block
        
        % Step 6: Store the decoded block
        blocks{blockIdx} = blockData;
        blockIdx = blockIdx + 1;
        
        % Exit if we have processed all blocks
        if blockIdx > expectedBlocks
            break;
        end
    end
    
    % Step 7: Check for padding or mismatched number of blocks
    if blockIdx ~= expectedBlocks + 1
        error('Mismatch in the number of blocks.');
    end
    
    % Step 8: Reconstruct the image from blocks
    image = reconstructImage(blocks, W_blocks, H_blocks, imgType);
    
    % Step 9: Save the image
    outputFilename = strcat(filename, '_decoded.png'); % Assuming the output is a PNG image
    imwrite(image, outputFilename);
    
    fclose(fid);
end

% Function to read and reconstruct the Huffman table
function huffmanTable = readHuffmanTable(fid, tableSize)
    % Read the Huffman table from the file (assuming it is stored in a specific format)
    % This part depends on how you saved the Huffman table during encoding
    huffmanTable = cell(tableSize, 2);
    
    for i = 1:tableSize
        symbol = fread(fid, 1, 'ubit16'); % Assuming symbol is stored as 16 bits
        codeword = fread(fid, 1, 'ubit16'); % Assuming codeword is stored as 16 bits
        huffmanTable{i, 1} = symbol;
        huffmanTable{i, 2} = dec2bin(codeword, 16); % Store the codeword as a binary string
    end
end

% Function to decode a single block using the Huffman table
function blockData = decodeBlock(fid, huffmanTable)
    blockData = [];
    while true
        % Read a symbol based on the Huffman table's codewords
        % This will require a bit-level decoding algorithm that matches the codewords
        % For simplicity, we assume the function huffmanDecode exists (implement it as needed)
        
        symbol = huffmanDecode(fid, huffmanTable);
        
        % If the EOB symbol is found, break the loop
        if symbol == 65535 % EOB symbol
            break;
        end
        
        % Append the symbol to the block data
        blockData = [blockData, symbol];
    end
end

% Function to decode the entire image from blocks
function image = reconstructImage(blocks, W_blocks, H_blocks, imgType)
    if imgType == 0
        % For grayscale, reconstruct the image as a 2D matrix
        image = reshape(cell2mat(blocks), [H_blocks * 8, W_blocks * 8]);
    else
        % For color, reconstruct the image with 3 channels (Y, Cb, Cr)
        Y = reshape(cell2mat(blocks(1:W_blocks*H_blocks)), [H_blocks * 8, W_blocks * 8]);
        Cb = reshape(cell2mat(blocks(W_blocks*H_blocks+1:2*W_blocks*H_blocks)), [H_blocks * 8, W_blocks * 8]);
        Cr = reshape(cell2mat(blocks(2*W_blocks*H_blocks+1:end)), [H_blocks * 8, W_blocks * 8]);
        
        % Convert YCbCr to RGB
        image = ycbcr2rgb(cat(3, Y, Cb, Cr));
    end
end

