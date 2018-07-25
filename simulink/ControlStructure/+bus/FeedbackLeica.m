function bus = FeedbackLeica()

n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'pos';
elems(n).Dimensions = 3;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 2;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R11';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 3;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R12';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 4;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R13';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 5;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R21';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 6;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R22';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 7;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R23';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 8;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R31';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 9;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R32';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 10;
elems(n) = Simulink.BusElement;
elems(n).Name = 'R33';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

bus = Simulink.Bus;
bus.Elements = elems;

end