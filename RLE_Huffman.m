function zigzagList = zigzagOrder(matrix)
    % Generate the zig-zag order for an 8x8 matrix
    zigzagIndices = [
         1  2  6  7 15 16 28 29;
         3  5  8 14 17 27 30 43;
         4  9 13 18 26 31 42 44;
        10 12 19 25 32 41 45 54;
        11 20 24 33 40 46 53 55;
        21 23 34 39 47 52 56 61;
        22 35 38 48 51 57 60 62;
        36 37 49 50 58 59 63 64];
    % Reshape into a 1D list following the zig-zag order
    zigzagList = matrix(zigzagIndices);
end

function matrix = inverseZigzag(zigzagList)
    % Ensure the input is a list of 64 elements
    if length(zigzagList) ~= 64
        error('Input must be a list of 64 elements.');
    end

    % Predefined zig-zag indices for an 8x8 matrix
    zigzagIndices = [
         1  2  6  7 15 16 28 29;
         3  5  8 14 17 27 30 43;
         4  9 13 18 26 31 42 44;
        10 12 19 25 32 41 45 54;
        11 20 24 33 40 46 53 55;
        21 23 34 39 47 52 56 61;
        22 35 38 48 51 57 60 62;
        36 37 49 50 58 59 63 64];

    % Create an empty 8x8 matrix
    matrix = zeros(8, 8);

    % Assign values from the zig-zag list back to the matrix
    matrix(zigzagIndices) = zigzagList;
end


function bitStream = modifiedHuffmanEncode(data)
    % Inputs:
    %   data - A list of 64 integers (the quantized and zig-zag ordered block)
    % Outputs:
    %   bitStream - The encoded bit stream as a character array
    %   huffmanTable - The Huffman table used for encoding (preorder traversal)

    % Step 1: Add EOB character to the data
    EOB = 65535; % Assign a large value for EOB (outside the usual data range)
    nonZeroData = data(1:find(data, 1, 'last')); % Trim trailing zeros
    if isempty(nonZeroData) % If all values are zero, only include EOB
        trimmedData = [EOB];
    else
        trimmedData = [nonZeroData, EOB];
    end

    % Step 2: Generate frequency table (include EOB)
    uniqueSymbols = unique(trimmedData);
    freqTable = arrayfun(@(x) sum(trimmedData == x), uniqueSymbols);

    % Step 3: Create Huffman table
    [symbols, probabilities] = deal(uniqueSymbols, freqTable / sum(freqTable));
    [huffmanDict, avgLen] = huffmandict(symbols, probabilities); %#ok<ASGLU>
    
    % Huffman dictionary format: {symbol, codeword}
    huffmanTable = huffmanDict;

    % Step 4: Encode the Huffman table into a bit stream
    bitStream = ''; % Initialize as a string for concatenation
    
    % Add the number of bits used to encode the Huffman table
    tableSizeBits = dec2bin(numel(huffmanDict) * 16, 16); % 16 bits for size
    bitStream = [bitStream, tableSizeBits]; % Concatenate as string
    
    % Serialize Huffman table in preorder (symbol and codeword pairs)
    for i = 1:size(huffmanDict, 1)
        symbolBits = dec2bin(huffmanDict{i, 1}, 16); % Encode symbol as 16-bit
        codeBits = char(huffmanDict{i, 2} + '0');    % Convert binary to string
        bitStream = [bitStream, symbolBits, codeBits]; % Append
    end

    % Step 5: Encode the data using the Huffman dictionary
    for value = trimmedData
        % Find the code for the current value
        idx = find(cellfun(@(x) isequal(x, value), huffmanDict(:, 1)));
        if isempty(idx)
            error('Value %d not found in Huffman dictionary.', value);
        end
        code = huffmanDict{idx, 2};
        codeBits = char(code + '0'); % Convert binary to string
        bitStream = [bitStream, codeBits]; % Append to bit stream
    end
end



% Input data (64 integers from an 8x8 block)
data = [16, 11, 10, 16, 24, 40, 51, 61, ...
        12, 12, 14, 19, 26, 58, 60, 55, ...
        14, 13, 16, 24, 40, 57, 69, 56, ...
        14, 17, 22, 29, 51, 87, 80, 62, ...
        18, 22, 37, 56, 68, 109, 103, 77, ...
        24, 35, 55, 64, 81, 104, 113, 92, ...
        49, 64, 78, 87, 103, 121, 120, 101, ...
        72, 92, 95, 98, 112, 100, 103, 99];

% Call the modified Huffman encoder
[bitStream, huffmanTable] = modifiedHuffmanEncode(data);

% Display the results
fprintf('Encoded Bit Stream:\n%s\n', num2str(bitStream));
disp('Huffman Table:');
disp(huffmanTable);
