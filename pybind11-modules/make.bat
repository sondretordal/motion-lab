echo off
if "%1" == "" goto COMPILE

if "%1" == "clean" goto CLEAN

if "%1" == "config" goto CONFIG
echo on


:COMPILE
cd build
cmake --build . --config Release
cd ..
echo Compile done!
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

:DONE
