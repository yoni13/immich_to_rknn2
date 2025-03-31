#!/bin/bash

python3 build_rknn.py "$1" "$2" > immich_to_rknn2.log

python_exit_status=$?

if [ $python_exit_status -ne 0 ]; then
    echo -e "\e[31mError: Python script failed with exit code $python_exit_status.\e[0m"
    echo "Check immich_to_rknn2.log for Python errors or details."
    cat immich_to_rknn2.log
    echo "Error_analysis.log"
    cat ./snapshot/error_analysis.txt
    echo "Map name to file"
    cat ./snapshot/map_name_to_file.txt
    exit $python_exit_status
fi

# if "No lowering found for" found in log file, return error status 1
if grep -q "No lowering found for" immich_to_rknn2.log; then
    echo -e "\e[31mSome operations are not supported by RKNN, please check the log file for details.\e[0m"
    cat immich_to_rknn2.log
    cat ./snapshot/error_analysis.txt
    cat ./snapshot/map_name_to_file.txt
    exit 1
else
    echo -e "\e[32mConversion completed successfully.\e[0m"
    # rm immich_to_rknn2.log
    exit 0
fi
