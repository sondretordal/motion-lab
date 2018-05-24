function bus = FeedbackStewart()

n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'eta';
elems(n).Dimensions = 6;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 2;
elems(n) = Simulink.BusElement;
elems(n).Name = 'eta_t';
elems(n).Dimensions = 6;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 3;
elems(n) = Simulink.BusElement;
elems(n).Name = 'eta_tt';
elems(n).Dimensions = 6;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

bus = Simulink.Bus;
bus.Elements = elems;

end