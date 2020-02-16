using System.Collections;
using System.Collections.Generic;
using UnityEngine;


using System.Runtime.InteropServices;
using System.IO;


public class DllTest : MonoBehaviour
{
    [DllImport("animallib", EntryPoint = "TestMultiply")]
    public static extern float DllTestMultiply(float a, float b);

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log(DllTestMultiply(2, 2));
    }
}
