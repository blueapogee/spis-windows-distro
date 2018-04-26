
HERE=`pwd`
echo $HERE

##############################################
#  Converter lib path
##############################################
GLOBAL_PARAM_CONVERTER_JAR_PATH=${HERE}/lib/globalParam.jar

##############################################
# Keridwen related stuff (should be adapted 
# to your Keridwen installation) 
##############################################
KERIDWEN_JAR_PATH=${HERE}/../../dependencies/main/org-keridwen-modelling-global-parameters-2.0.0.jar

##############################################
# Stream stuff
##############################################
XSTREAM_JAR_PATH=${HERE}/../../dependencies/main/org-keridwen-xstream-2.0.0.jar

##############################################
# Jython stuff (should be adapted to your 
# local Jython installation)
##############################################
JYTHON_HOME=${HERE}/../../dependencies/thirdparty/jython-2.5.1/
JYTHON_JAR_PATH=${HERE}/../../dependencies/main/jython-2.5.1.jar
PYTHON_MODULES_PATH=${JYTHON_HOME}/Lib/


##############################################
# Logging stuff
##############################################
SFL4J_PATH=${HERE}/dependencies/slf4j-1.5.8/
SHL4J_JAR_PATH=${SFL4J_PATH}/slf4j-api-1.5.8.jar:${SFL4J_PATH}/slf4j-log4j12-1.5.8.jar:${SFL4J_PATH}/slf4j-ext-1.5.8.jar
LOG4J=${HERE}/dependencies/apache-log4j-1.2.15/log4j-1.2.15.jar

##############################################
#  SPIS-LEGACY struff
##############################################
SPIS_LEGACY_MODULES_PATH=${HERE}/SpisLegacy

##############################################
# Command line
##############################################
${HERE}/../../dependencies/thirdparty/jre-1.6.0_22-linux64b/bin/java -cp .:${GLOBAL_PARAM_CONVERTER_JAR_PATH}:${JYTHON_JAR_PATH}:${KERIDWEN_JAR_PATH}:${XSTREAM_JAR_PATH}:${SPIS_LEGACY_MODULES_PATH}:${SHL4J_JAR_PATH}:${LOG4J} -Dpython.home=${JYTHON_HOME} -Dpython.path=:${SPIS_LEGACY_MODULES_PATH}/Modules:${SPIS_LEGACY_MODULES_PATH}/Bin:${SPIS_LEGACY_MODULES_PATH}/Modules/Adapter org.python.util.jython scriptExportGlobal.py $1 $2


