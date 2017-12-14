close all
clear all
clc

% Load csv data into table format
data = readtable('variablelist.csv');

fileRxMru = fopen('RxMru.txt', 'w');
fileVarString = fopen('VarString.txt', 'w');

fprintf(fileRxMru, 'mruOK : BYTE; // Mru Status, 113=OK\n');
fprintf(fileRxMru, 'dataLength : BYTE; // Data length\n');
fprintf(fileRxMru, 'token : BYTE; // MRU token\n');

N = length(data.VarName);
for i = 1:N
        
    fprintf(fileRxMru, '%s : %s; // No. %s - %s - %s\n',...
        data.VarName{i},...
        data.DataType{i},...
        num2str(data.VarNumber(i)),...
        data.Unit{i},...
        data.Description{i});

    fprintf(fileVarString, '%s ', num2str(data.VarNumber(i)));
    
end

fprintf(fileRxMru, 'checksum : BYTE; // Data checksum \n');

fclose(fileRxMru);
fclose(fileVarString);