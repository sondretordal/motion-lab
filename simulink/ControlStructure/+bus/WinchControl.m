function bus = WinchControl()

n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'length';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 2;
elems(n) = Simulink.BusElement;
elems(n).Name = 'length_t';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 3;
elems(n) = Simulink.BusElement;
elems(n).Name = 'length_tt';
elems(n).Dimensions = 1;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

bus = Simulink.Bus;
bus.Elements = elems;

end