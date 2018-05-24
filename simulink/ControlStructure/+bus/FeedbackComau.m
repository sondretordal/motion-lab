function bus = FeedbackComau()

n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'q';
elems(n).Dimensions = 3;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

n = 2;
elems(n) = Simulink.BusElement;
elems(n).Name = 'q_t';
elems(n).Dimensions = 3;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

bus = Simulink.Bus;
bus.Elements = elems;

end