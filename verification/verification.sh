#!/bin/bash
# Usage: bash /path/to/verification.sh

#Import functions (import all fds files)
#Usage: import_test_fds "/path/to/input/folder" "/path/to/output/folder/"
import_test_fds () {

    #Importing Verification tests from FDS
    for d in $1*/ ; do
        echo "Found new case: $d"

        case_name=$(basename $d)
        path_in=$1$case_name
        path_out=$2$case_name

        echo "case: $case_name"
        echo "path in: $path_in"
        echo "path out: $path_out"

        #Removing test if present
        if [ -d $path_out ]
        then
            echo "REMOVE: $path_out"
            rm -r $path_out
        fi

        #Copying fds files
        mkdir -p $path_out"/FDS_Input_Files"
        find $path_in -name '*.fds' -execdir cp "{}" $path_out"/FDS_Input_Files/" ";"

        #Creation of test.xml file
        #N.B.: to avoit XML parser installation we use echo
        echo '<?xml version="1.0"?>'     >> $path_out/test.xml 
        echo '<testType>'                >> $path_out/test.xml
        echo '   <blnfds>false</blnfds>' >> $path_out/test.xml 
        echo '   <fdsfds>true</fdsfds>'  >> $path_out/test.xml 
        echo '</testType>'               >> $path_out/test.xml 

    done
} 

#System variables
CWD="$(pwd)/"
TEMP_PATH="/var/tmp/fds_tmp/"
BLENDER_PATHFILE="/opt/blender/blender"
FDS_PATH="/opt/FDS/FDS6/bin"	

#Local copy of FDS git repository
rm -rf $TEMP_PATH
mkdir -p $TEMP_PATH
git clone https://github.com/firemodels/fds.git --branch master --single-branch $TEMP_PATH

#Tests import
import_test_fds "${TEMP_PATH}Verification/" $CWD
import_test_fds "${TEMP_PATH}Validation/" $CWD

# FDS setup
echo "FDS setup..."
ulimit -s unlimited
ulimit -v unlimited
source $FDS_PATH//FDS6VARS.sh
source $FDS_PATH//SMV6VARS.sh
export OMP_NUM_THREADS=1

# Running Blender
echo "Run verification.py in Blender..."
"${BLENDER_PATHFILE}" --background --python "${CWD}verification.py" &> error.log

#rm error.log
