echo off
if "%1" == "" goto COMPILE

if "%1" == "clean" goto CLEAN

if "%1" == "config" goto CONFIG

if "%1" == "update" goto UPDATE
echo on


:COMPILE
if exist build (
    cd build
    cmake --build . --config Release
    cd ..
    echo Compile done!
) else (
    echo Run "make config" before running "make" command!
)
goto DONE

:CLEAN
if exist build (
    rm -rd build
    echo Clean done!
) else (
    echo Already clean!
)
goto DONE

:CONFIG
mkdir build 
cd build
conan install ..
cmake .. -G "Visual Studio 14 2015 Win64"
type NUL > __init__.py
cd ..
echo Config done!
goto DONE

:UPDATE
if exist build  (
    cd build
    cp MotionLab.pyd ../../hmi/src/MotionLab.pyd
    cd ..
    echo Python module updated
    goto DONE
)


:DONE
