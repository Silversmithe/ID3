#!/bin/bash

MYNAME=`basename "$0"`

if [ "$#" -ne '1' ]
then
  echo "Usage: $MYNAME <test_directory>" 1>&2
  exit 1
fi

TEST_DIR="$1"
RESULTS_DIR="test_results"

die() {
  echo "$1" 1>&2
  exit 1
}

mkdir -p $RESULTS_DIR || die "Failed to create $RESULTS_DIR"

RESULT_PASS=0
RESULT_FAIL_TO_RUN=0
RESULT_FAIL_TO_COMPARE=0
TEST_NUM=1

echo

for test_filename in `ls -1 $1 | grep '\.out$' | sort`
do
  testname=`basename $test_filename .out`
  full_filename="$TEST_DIR/$test_filename"

  # Verify that attributes file exists. By default, the classifier is
  # the last attribute in the file.
  attr_filename="${TEST_DIR}/${testname}-attributes.txt"
  if ! [ -f "$attr_filename" ]
  then
    die "Cannot find attributes file $attr_filename for test $testname"
  fi
  classifier=`tail -1 $attr_filename | sed -e 's/:.*$//'`

  # Verify that training data file exists
  train_data_filename="${TEST_DIR}/${testname}-train.csv"
  if ! [ -f "$train_data_filename" ]
  then
    die "Cannot file training file $train_data_filename for test $testname"
  fi

  test_data_filename="${TEST_DIR}/${testname}-test.csv"

  echo -n "TEST $TEST_NUM ($test_filename)..."
  TEST_NUM=$((TEST_NUM+1))
  test_out_filename="$RESULTS_DIR/${testname}.out"
  if [ -f "$test_data_filename" ]
  then
    python ./main.py id3 \
                     "$classifier" \
                     --attributes "$attr_filename" \
                     --train "$train_data_filename" \
                     --test "$test_data_filename" \
           > $test_out_filename 2>&1
  else
    python ./main.py id3 \
                     "$classifier" \
                     --attributes "$attr_filename" \
                     --train "$train_data_filename" \
           > $test_out_filename 2>&1
  fi

  if [ "$?" -ne '0' ]
  then
    echo "FAILED TO RUN"
    RESULT_FAIL_TO_RUN=$((RESULT_FAIL_TO_RUN+1))
    continue
  fi

  if ! cmp -s "$test_out_filename" "$full_filename"
  then
    echo "FAIL"
    RESULT_FAIL_TO_COMPARE=$((RESULT_FAIL_TO_COMPARE+1))
    continue
  fi

  echo "PASS"
  RESULT_PASS=$((RESULT_PASS+1))
done

echo
echo "SUMMARY"
echo "~~~~~~~"
echo "PASSES: $RESULT_PASS"
echo "FAILURES: $RESULT_FAIL_TO_COMPARE"
echo "FAILED TO RUN: $RESULT_FAIL_TO_RUN"
echo

