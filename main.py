#!/usr/bin/python

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
parser.add_argument('--train',
                    type=argparse.FileType('r'),
                    help='Name of the file to use for training',
                    dest='training_file',
                    required=True)
parser.add_argument('--test',
                    type=argparse.FileType('r'),
                    dest='testing_file',
                    help='Name of the file to use for testing')
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

# Train
training_data = dataset.DataSet(args.training_file, all_attributes)
starting_attrs = copy.copy(all_attributes)
starting_attrs.remove(classifier)
dtree = dtree_pkg.DTree(classifier, training_data, starting_attrs)
print dtree.dump()

if args.testing_file:
  testing_data = dataset.DataSet(args.testing_file, all_attributes)
  correct_results = dtree.test(classifier, testing_data)
  print("%d of %d (%.2f%%) of testing examples correctly identified" %
        (correct_results, len(testing_data),
         (float(correct_results) * 100.0)/ float(len(testing_data))))

