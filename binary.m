bitString = '1100101011110001010101101'; % Example bit string

% Ensure the bit string length is a multiple of 8
paddingLength = mod(-length(bitString), 8); % Find how many bits to pad
bitString = [bitString, repmat('0', 1, paddingLength)]; % Pad with zeros if necessary

% Convert bit string to numeric bytes
byteArray = uint8(bin2dec(reshape(bitString, 8, []).')); % Group into bytes and convert to decimal

% Save to a binary file
fileID = fopen('output.bin', 'w'); % Open file for writing
fwrite(fileID, byteArray, 'uint8'); % Write the byte array as binary
fclose(fileID); % Close the file

disp('Bit string saved as binary file: output.bin');
fileID = fopen('output.bin', 'r');
byteArray = fread(fileID, 'uint8');
fclose(fileID);
% Convert back to bit string
retrievedBitString = reshape(dec2bin(byteArray, 8).', 1, []);
disp(retrievedBitString);

%%%%%%%%%%%%%%%%%%

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

function bitString = retrieveBitString(filename)
    fileID = fopen(filename, 'r');
    if fileID == -1
        error('Could not open file: %s', filename);
    end

    byteArray = fread(fileID, 'uint8');
    fclose(fileID);

    % Convert the byte array back to a bit string
    bitString = reshape(dec2bin(byteArray, 8).', 1, []); % Convert each byte to 8-bit binary and reshape
    fprintf('Bit string retrieved from binary file: %s\n', filename);
end