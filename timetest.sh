#!/bin/env bash
set -eu

NUMBER_OF_RUNS=10
TEST_FILE="functiontest.py"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color


if [ ! -f "$TEST_FILE" ]; then
    echo "$TEST_FILE does not exist."
    exit 1
fi

declare -a ARRAY

printf "Time is in seconds\n\n"
echo "**Testing $TEST_FILE - $NUMBER_OF_RUNS times**"

COUNTER=0
while [ "$COUNTER" -lt "$NUMBER_OF_RUNS" ]
do
    execution_string="$(python3 $TEST_FILE)"
    echo $execution_string
    ARRAY+=($(echo $execution_string | sed -e 's/.*=//' -e 's/ .*$//'))
    COUNTER=$[$COUNTER +1]
done

# i.e (0.007777690887451172 + 0.007235050201416016 + 0.007931709289550781 + 0.009009361267089844 + 0.008493185043334961)
time_array_with_plus="($(echo ${ARRAY[*]} | sed 's/ / + /g'))"

average_time=$(echo "( $time_array_with_plus ) / $NUMBER_OF_RUNS" | bc -l)

printf "\n${GREEN}%.2E${NC}${CYAN} -> ${NC}${YELLOW}average${NC}${CYAN}=${NC}${GREEN}%.12F\n${NC}" $average_time $average_time
