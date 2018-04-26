@echo off

:: compute the directory where the command is launche (pwd equivalent)
SET STARTPOINT=%cd%
::echo "STARTPOINT"%STARTPOINT%

:: compute the name of the .batch script
set batchScriptName=%~nx0
::echo "batchScriptName"%batchScriptName%

:: compute the path of the .bat script
SET mypath=%~dp0
::echo "mypath"%mypath%

:: go to directory where is defined the path of the .bat script
pushd %mypath%

:: compute the number of arguments
set argumentNumber=0
for %%x in (%*) do Set /A argumentNumber+=1
::echo "argumentNumber"%argumentNumber%

::  # test if an argument exist
if %argumentNumber% == 0 goto noArgumentExist
if not %argumentNumber% == 0 goto argumentExist

:argumentExist
::echo "argumentExist"
::    # test if more than 1 argument exist (used with -h option)
if  %argumentNumber% == 1 goto noArgumentExist
if not %argumentNumber% == 1 goto moreOneArgumentExist

:moreOneArgumentExist
::echo "moreOneArgumentExist"
:: compute the first character of the argument
set secondCharacter=%2
::echo "secondCharacter"%secondCharacter%
set secondCharacter=%secondCharacter:~1,1%
::echo "secondCharacter"%secondCharacter%
:: compute the path where the command is launched
if %secondCharacter% == : (
:: the argument is defined with an absolute path
  set PATH_CORRECTED=%2 
  rem echo "PATH_CORRECTED"%PATH_CORRECTED%
)
if not %secondCharacter% == : (
  :: the argument is defined with a relative path
  set PATH_CORRECTED=%STARTPOINT%\%2  
  rem echo "PATH_CORRECTED"%PATH_CORRECTED%
)

:noArgumentExist
::echo "noArgumentExist"

set FormatedTime=%Time: =0%
set NOW=%date:~-4,4%%date:~-7,2%%date:~-10,2%%FormatedTime:~-11,2%%FormatedTime:~-8,2%%FormatedTime:~-5,2%%FormatedTime:~-2,2%

if %argumentNumber% == 0 (

::echo "?"
%JAVA_HOME%\bin\java.exe -Xmx2048M -splash:resources/images/splash_spis-geo-png24.png -jar -Dspis.timestamp=%NOW% -Dlogback.configurationFile=resources/logging/logback.xml -Dfelix.config.properties=file:resources/felix/config.properties -Dactivate3DViews=false -Dorg.keridwen.config=./resources/org-spis-geo-win7-64b.properties dependencies\thirdparty\felix-5.0.1\felix.jar

goto EOF

)

if %1 == -p (

::echo "p"
%JAVA_HOME%\bin\java.exe -Xmx2048M -jar -Djava.awt.headless=true -Dspis.timestamp=%NOW% -Dlogback.configurationFile=resources/logging/logback-headless.xml -Dfelix.config.properties=file:resources/felix/config.properties -Dactivate3DViews=false -Dorg.keridwen.config=./resources/org-spis-geo-win7-64b.properties -Dorg.keridwen.headless=true -Dorg.spis.batch.project.path=%PATH_CORRECTED% dependencies\thirdparty\felix-5.0.1\felix.jar

goto EOF

)

if %1 == -b (

::echo "b"
%JAVA_HOME%\bin\java.exe -Xmx2048M -jar -Djava.awt.headless=true -Dspis.timestamp=%NOW% -Dlogback.configurationFile=resources/logging/logback-headless.xml -Dfelix.config.properties=file:resources/felix/config.properties -Dactivate3DViews=false -Dorg.keridwen.config=./resources/org-spis-geo-win7-64b.properties -Dorg.keridwen.headless=true -Dorg.spis.batch.script.path=%PATH_CORRECTED% dependencies\thirdparty\felix-5.0.1\felix.jar

goto EOF

)

if %1 == -h (

::echo "h"
echo "Usage:\n"
echo "* To run SPIS with its graphical user interface:"
echo %batchScriptName%
echo "* To run SPIS in batch mode and execute a simulation from a given SPIS project:"
echo %batchScriptName%" -p path\to\project.spis5"
echo "* To run SPIS in batch mode and execute a given Jython script:"
echo %batchScriptName%" -b path\to\jython\script"

goto EOF

)

if %1 == -m (

::echo "m"
%JAVA_HOME%\bin\java.exe -Xmx2048M -splash:resources/images/splash_spis-geo-png24.png -jar -Dspis.timestamp=%NOW% -Dlogback.configurationFile=resources/logging/logback.xml -Dfelix.config.properties=file:resources/felix/config.properties -Dactivate3DViews=false -Dorg.keridwen.config=./resources/org-spis-geo-win7-64b.properties -DforceLAF=Metal dependencies\thirdparty\felix-5.0.1\felix.jar

goto EOF

)

:EOF