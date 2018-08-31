function bus = ControlStewart()

n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'eta';
elems(n).Dimensions = 6;
elems(n).DimensionsMode = 'Fixed';
elems(n).DataType = 'double';
elems(n).SampleTime = -1;
elems(n).Complexity = 'real';

bus = Simulink.Bus;
bus.Elements = elems;

end