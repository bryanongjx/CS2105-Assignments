#!/bin/bash

# colors
NOCOLOR='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHTGRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
LIGHTRED='\033[1;31m'
LIGHTGREEN='\033[1;32m'
YELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
LIGHTPURPLE='\033[1;35m'
LIGHTCYAN='\033[1;36m'
WHITE='\033[1;37m'

d0="$(dirname "$(readlink -f -- "$0")")"

fname="Integrity"
source "$d0/common.sh"

mkdirTmp
findPy3

#d1="/home/course/cs2105/autotest/a1"
#d1="$d0/.."

mac_f_name="$d0/mac.key"

num_test=0
passed_test=0

######################
run() {
  ((num_test++))
  echo "--------- running test $1 --------------"
  program_output=$(eval exec "$evalcmd" "$mac_f_name" "$cdir/$1.in")
  expected_output=$(cat "$cdir/$1.out")
  echo -e "Program  output: ${RED}$program_output${NOCOLOR}"
  echo -e "Expected output: ${GREEN}$expected_output${NOCOLOR}"
  if [[ "$program_output" == "$expected_output" ]]
  then
    ((passed_test++))
    echo -e "${GREEN}Passed${NOCOLOR}"
  else
    echo -e "${RED}Failed${NOCOLOR}"
  fi
  echo
#  (eval exec "$evalcmd" $1 2> "$tmpdir/s-err")
}

cdir="$d0/cases"
if [[ -z "$arg1" ]]; then
  # if we provide no argument ot hte test scrip, run all test cases
  case_id=1
  while [[ -f "$cdir/$case_id.in" ]]; do
    run "$case_id"
    ((case_id++))
  done
else
  # if we provide one argument, run that particular testcase
  if [ -f "$cdir/$arg1.in" ]
  then
    run "$arg1"
  else
    echo "Unknown testcase $arg1"
  fi
fi
echo -e "PASSED ${GREEN}$passed_test/$num_test${NOCOLOR}"