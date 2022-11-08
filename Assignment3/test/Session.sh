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

fname="Session"
source "$d0/common.sh"

mkdirTmp
findPy3

#d1="/home/course/cs2105/autotest/a1"
#d1="$d0/.."

out_file_key=$tmpdir/cs2105_ice.key
out_file_data=$tmpdir/cs2105_ice.data
host_id="cs2105-i.comp.nus.edu.sg"
port_num=9999

correct_file="$d0"/input.txt
######################
run() {
  echo "--------- running test --------------"
  (eval exec "$evalcmd" "$out_file_key" "$out_file_data" "$host_id" "$port_num")

  # compare key
#  program_output=$(cat "$out_file_key")
#  expected_output=$(cat "$d0"/session.key)
  program_output=$(xxd "$out_file_key")
  expected_output=$(xxd "$d0"/session.key)
  echo -e "Program  output key: ${RED}$program_output${NOCOLOR}"
  echo -e "Expected output Key: ${GREEN}$expected_output${NOCOLOR}"
  if [[ "$program_output" == "$expected_output" ]]
  then
    echo -e "Key  ${GREEN}Match${NOCOLOR}"
  else
    echo -e "Key  ${RED}Mismatch${NOCOLOR}"
  fi
  echo

  # compare data
  if cmp --silent "$correct_file" "$out_file_data"; then
    echo -e "Data ${GREEN}Match${NOCOLOR}"
  else
    echo -e "Data ${RED}Mismatch${NOCOLOR}"
  fi
  echo
}

run
