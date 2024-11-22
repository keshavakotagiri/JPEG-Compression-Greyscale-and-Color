
filename = 'kodak24';
% filename_compressed = 'compressed';
fileInfo = dir([filename '.jpg']); % Replace 'filename.ext' with your file name
fileSize = fileInfo.bytes;     % Get the file size in bytes
fprintf('The size of %s.jpg is %d bytes.\n', filename, fileSize);
% Load the image into MATLAB



% Call the compress function with the image matrix and the compression parameters
compress([filename '.jpg'], [4 2 2]);  % Pass the image matrix and parameters for compression

% in between also we will probably do something like check up size of
% binary file to see how less space it takes.

% decompress([filename '.bin'])
% 
% fileInfo = dir([filename_compressed '.jpg']);
% fileSize_compressed = fileInfo.bytes;     % Get the file size in bytes
% fprintf('The size of %s.jpg is %d bytes.\n', filename, fileSize_compressed);
% 
% img = imread([filename '.jpg']);
% img = double(img);
% 
% img_compressed = imread([filename_compressed '.jpg']);
% img_compressed = double(img_compressed);
% 
% mse = mean((img - img_compressed).^2, 'all');