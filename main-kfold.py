#!/usr/bin/python
"""
File:           main-kfold.py

Author:         Alexander S. Adranly

Provides a command-line interface to the decision tree. It takes a positional
parameter for the decision tree algorithm module name, and for the name of the classification
attribute. Invoke with --help to see the complete list of options.

Improves measurement of accuracy of ML algorithm

PROMPT:
Implement k-fold validation by running k iterations, each time using a different partition of the data for training
and testing. Note that this will require changes to the main.py interface, so please create a separate
main-kfold.py
"""

import argparse
import copy
import sys

import attributes
import dataset

parser = argparse.ArgumentParser(
           description='Train (and optionally test) a decision tree')
parser.add_argument('dtree_module',
                    metavar='dtree-module',
                    help='Decision tree module name')
parser.add_argument('classifier',
                    help='Name of the attribute to use for classification')
parser.add_argument('--attributes',
                    type=argparse.FileType('r'),
                    help='Name of the attribute specification file',
                    dest='attributes_file',
                    required=True)
parser.add_argument('--data',
                    type=argparse.FileType('r'),
                    help='Name of the file with all of the data',
                    dest='data_file',
                    required=True)
parser.add_argument('--k_value',
                    dest='k_value',
                    help='Number of partitions')
args = parser.parse_args()

# Read in a complete list of attributes.
# global all_attributes
all_attributes = attributes.Attributes(args.attributes_file)
if args.classifier not in all_attributes.all_names():
  sys.stderr.write("Classifier '%s' not a recognized attribute name\n" %
                   args.classifier)
  sys.exit(1)
classifier = all_attributes[args.classifier]

# Import the d-tree module, removing the .py extension if found
if args.dtree_module.endswith('.py') and len(args.dtree_module) > 3:
  dtree_pkg = __import__(args.dtree_module[:-3])
else:
  dtree_pkg = __import__(args.dtree_module)


# FUNCTION DEFINITIONS
#  crawling internals
def _generate_example(example_data):
    """
    :param dir_list: str[] : a list of filepath information to distribute
    :return: item : an indexed item from an iterable object

    description: a generator to distribute any information necessary
    """
    for example in example_data:
        yield example

# Train
data = dataset.DataSet(args.data_file, all_attributes)
starting_attrs = copy.copy(all_attributes)
starting_attrs.remove(classifier)
k_value = int(args.k_value)
if k_value <= 1:
    print 'warning: a partition of 1 or less will not work'
    print 'using k_value = 2'
    k_value = 2

# create K DATA SETS
data_partition = list()
for i in range(0, k_value):
    data_partition.append(dataset.DataSet())

# ROUND ROBIN ADD EXAMPLES
example_generator = _generate_example(example_data=data.all_examples)  # generator for examples
try:
    while True:
        for partition in data_partition:
            partition.append(next(example_generator))
except StopIteration:
    # example distribution is complete
    pass

# K-FOLD PARTITIONING
k_fold_forest = []  # a forest of d trees
test_accuracy_sum = 0  # variable to hold the sum of each training and testing
for testing_partition in data_partition:
    # use the selected partition for the training set
    # group all the other partitions into a testing set
    training_dataset = [x for x in data_partition if x != testing_partition]
    train_set = dataset.DataSet()

    for dset in training_dataset:
        train_set.all_examples.extend(dset.all_examples)

    # train the tree and gather the results
    k_fold_forest.append(dtree_pkg.DTree(classifier, train_set, copy.copy(starting_attrs)))

    # test the tree
    correct_results = k_fold_forest[-1].test(classifier, testing_partition)
    accuracy = (float(correct_results)*100.0)/float(len(testing_partition))
    test_accuracy_sum += accuracy

# DISPLAY AVERAGE
print "On average: {}% of the testing examples were correctly identified".format(float(test_accuracy_sum/float(k_value)))
