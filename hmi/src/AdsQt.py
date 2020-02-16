from ctypes import sizeof, addressof, c_ubyte, Structure, memmove
import pyads
import struct
from pyads.structs import SAdsNotificationHeader

# Modified version of Connection.notification
def notification(plc_datatype=None, pyqtSignal=None):
    # type: (Optional[Type[Any]]) -> Callable
    """Decorate a callback function.

    **Decorator**.

    A decorator that can be used for callback functions in order to
    convert the data of the NotificationHeader into the fitting
    Python type.

    :param plc_datatype: The PLC datatype that needs to be converted. This can
    be any basic PLC datatype or a `ctypes.Structure`.

    The callback functions need to be of the following type:

    >>> def callback(handle, name, timestamp, value)

    * `handle`: the notification handle
    * `name`: the variable name
    * `timestamp`: the timestamp as datetime value
    * `value`: the converted value of the variable

    **Usage**:

        >>> import pyads
        >>>
        >>> plc = pyads.Connection('172.18.3.25.1.1', 851)
        >>>
        >>>
        >>> @plc.notification(pyads.PLCTYPE_STRING)
        >>> def callback(handle, name, timestamp, value):
        >>>     print(handle, name, timestamp, value)
        >>>
        >>>
        >>> with plc:
        >>>    attr = pyads.NotificationAttrib(20,
        >>>                                    pyads.ADSTRANS_SERVERCYCLE)
        >>>    handles = plc.add_device_notification('GVL.test', attr,
        >>>                                          callback)
        >>>    while True:
        >>>        pass

    """
    def notification_decorator(func):
        # type: (Callable[[int, str, datetime, Any], None]) -> Callable[[Any, str], None] # noqa: E501

        def func_wrapper(notification, data_name):
            # type: (Any, str) -> None
            contents = notification.contents
            data_size = contents.cbSampleSize
            # Get dynamically sized data array
            data = (c_ubyte * data_size).from_address(
                addressof(contents) + SAdsNotificationHeader.data.offset
            )

            if plc_datatype == pyads.PLCTYPE_STRING:
                # read only until null-termination character
                value = bytearray(data).split(b"\0", 1)[0].decode("utf-8")


            elif issubclass(plc_datatype, Structure):
                value = plc_datatype()
                fit_size = min(data_size, sizeof(value))
                memmove(addressof(value), addressof(data), fit_size)

            elif plc_datatype not in pyads.DATATYPE_MAP:
                value = bytearray(data)

            else:
                value = struct.unpack(
                    pyads.DATATYPE_MAP[plc_datatype], bytearray(data)
                )[0]
            
            # QUICKFIX: dt is commented out since it outside the Connection class in my case
            # dt = filetime_to_dt(contents.nTimeStamp)
            dt = 0.0

            # Write data to signal
            pyqtSignal.emit(value)
            
            
            
            

            return func(contents.hNotification, data_name, dt, value)

        return func_wrapper

    return notification_decorator