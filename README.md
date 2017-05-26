# Homework \#3 - Machine Learning

COEN 266 - Artificial Intelligence

Spring 2017

### Overview
For this homework assignment, you will be implementing a decision tree that uses the ID3 algorithm.

## Part 1: Data Cleaning (20 points)
For this portion, you will need to develop a dataset comprised of at least 100 examples. If you would like, you can use one
of the data sets that are publicly available at: https://archive.ics.uci.edu/ml/.

The data should be comprised of categorical attributes and classifier. IF you find a data set you would like to use and it
contains numerical values, you can massage it into categorical form by partitioning the values into ranges (extra credit
can be had for implementing an algorithm that automatically performs this task, see late in the assignment).

You should also clean your data set by removing examples that have missing values (or figuring out a reasonable way to represent
them, perhaps by adding a different value, such as "unspecified"). Next, you will need to create exactly three files: an
attributes file, a training dataset file, and a testing dataset file.

### Attributes File
This file contains the list of all the attributes and their possible values (this will include the classifier and its values).
Each line in the attributes file should be in the format "attribute: value0, value1, ... valueN". For example:

    size: small, medium, large
    sharp teeth: yes, no
    feet: yes, no
    habitat: land, water
    domesticated: yes, no
    dangerour: yes, no
    
*Your data set should be unique to you.* Feel free to share it with other students for testing purposes, but they should
not also submit the same data set.

### Dataset Files
Each of the dataset files should have a list of examples, with one example per line. Each example is simply a comma-separated
list of values, one for each attribute in the order provided in the attributes file. There may also be a "name:" at the 
beginning of a line to use as a label for the data. These labels are optional and simply for readability: they are thrown 
away by the parser. Three lines from a dataset file may look like this:

    snake:small,yes,no,land,no,yes
    bear:medium,yes,yes,land,no,yes
    deer:medium,no,yes,land,no,no
    
Randomize the order of your examples (this is more important for some datasets than others, but it never hurts). This can
be easily accomplished with the *shuf* utility on the DC workstations.

Next, partition all of your examples in two dataset files, one to use for training the decision tree algorithm (training set)
and one for testing the effectiveness of your trained tree (testing set).

## Part 2: ID3 Decision Tree Creation and Testing (70 points)
Implement an ID3-based decision tree creator and tester. It will accept a set of data in the format described in part 1,
and from that data produce a decision tree. It will also allow testing the accuracy of the decision  tree by running test
cases against the tree and comparing the decision tree's performance against the known classifications.

In some cases, you will run out of attributes before uniformly classifying the examples (this can happen if more than one
example has the same attributes, but different classifications). Also, you can have the case where there are values in a 
decision tree for which there are no examples (this should only happen if you have attributes with more than two values).
The following guidelines describe appropriate handling of these cases.

*1. If you run out of attributes and there are examples with different classifications, choose the classification for which
there are the most examples. If there are a duplicate number of examples in more than one group, choose the classification
with the earliest alphabetical value (using python's native string comparisons).*

*2. If you have a subpopulation that has no examples for an attribute value, choose the most prevalent example from the
population that falls into the parent's domain, as per guideline 1.*

### Framework
You are provided the following source files to use in this assignment:

*main.py:* Provides a command-line interface to the decision tree. It takes positional parameter for the decision tree
algorithm module name, and for the name of the classification attribute. Invoke with --help to see complete list of options.
 
    Example 1: Use the DTree implementation found in id3.py, and invoke on the dangerous-animals training data,
    classifying based on the 'dangerous' attribute:
    
    $ ./main.py id3 dangerous --attributes tests/dangerous-animals-attributes.txt \ --train tests/kr-vs-kp-train.csv
    --test tests/kr-vs-kp-test.csv
    
    Example 2: Use the DTree implementation found in id3.py and invoke on the kr-vs-kp training data, classifying based on
    the 'white-can-win' attribute. After building the complete decision tree, run it against the test data and report its
    performance:
    
    $ ./main.py id3 white-can-win --attributes tests/kr-vs-kp-attributes.txt --train tests/kr-vs-kp-train..csv --test 
    tests/kr-vs-kp-test.csv
    
*attributes.py*: Specifies an interface for storing individual datapoints (class Example), and collections of datapoints 
(class DataSet). A DataSet can be initialized from a data file in the format described in section 1.

*dataset.py*: Specifies an interface for storing individual datapoints (class Example), and collections of datapoints 
(class DataSet). A DataSet can be initialized from a data file in the format described in the section 1.

In general, the provided files should not be modiied, with the exception of *dataset.py*, in which you should implement an
entropy calculation (the entropy method is stubbed in for the framework).

A starting point for id3.py is also provided, but is mostly unimplemented.

## API
You will need to implement the class DTree in the file id3.py. This class must implement at least the following methods:
