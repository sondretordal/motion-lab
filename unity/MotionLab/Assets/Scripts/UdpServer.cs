using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Runtime.InteropServices;
using UnityEngine;


public class UdpServer : MonoBehaviour {
    // UDP data
    public string remoteIp = "192.168.90.60";
    public int remotePort = 50060;
    public string localIp = "192.168.90.50";
    public int localPort = 50050;

    public int nRecieved = 0;

    public int rxSize = 0;
    public int txSize = 0;
    public byte[] rxBuffer;
    public byte[] txBuffer;

    // UDP socket
    UdpClient socket;

    public T BufferToStruct<T>(byte[] buffer) where T : struct
    {
        // https://stackoverflow.com/questions/2623761/marshal-ptrtostructure-and-back-again-and-generic-solution-for-endianness-swap

        T result = default(T);
        GCHandle handle = GCHandle.Alloc(buffer, GCHandleType.Pinned);

        try
        {
            IntPtr rxPtr = handle.AddrOfPinnedObject();
            result = (T)Marshal.PtrToStructure(rxPtr, typeof(T));
        }
        finally
        {
            handle.Free();
        }

        return result;
    }

    public byte[] StructToBuffer<T>(T str)
    {
        // https://stackoverflow.com/questions/2623761/marshal-ptrtostructure-and-back-again-and-generic-solution-for-endianness-swap

        byte[] buffer = new byte[Marshal.SizeOf(str)];

        GCHandle handle = GCHandle.Alloc(txBuffer, GCHandleType.Pinned);

        try
        {
            IntPtr txPtr = handle.AddrOfPinnedObject();
            Marshal.StructureToPtr(str, txPtr, false);
        }
        finally
        {
            handle.Free();
        }

        return buffer;
    }

    // Use this for initialization
    void Start () {
        // Start async UDP connection
        IPEndPoint localEP = new IPEndPoint(IPAddress.Parse(localIp), localPort);
        //socket = new UdpClient(localEP);
        socket = new UdpClient(localEP);
        socket.BeginReceive(new AsyncCallback(OnUdpData), socket);

        txBuffer = new byte[6];
    }

    void OnUdpData(IAsyncResult result)
    {
        // this is what had been passed into BeginReceive as the second parameter:
        UdpClient socket = result.AsyncState as UdpClient;
        
        // Recieve data from remote source
        IPEndPoint source = new IPEndPoint(IPAddress.Parse(remoteIp), remotePort);
        rxBuffer = socket.EndReceive(result, ref source);
        rxSize = rxBuffer.Length;

        
      
        // Send data back to remote soruce
        txSize = txBuffer.Length;
        socket.Send(txBuffer, txBuffer.Length, source);
        
        // schedule the next receive operation once reading is done:
        socket.BeginReceive(new AsyncCallback(OnUdpData), socket);

        // Increment counter
        nRecieved = nRecieved + 1;
    }

    void Update()
    {
        // Implement this one if needed

    }   


    void OnApplicationQuit()
    {
        // Close UDP connection
        socket.Close();
    }
}

