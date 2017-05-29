#!/usr/bin/python

import argparse
import copy
import sys

import attributes
import dataset
from id3 import Node

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

print "d-tree module: ", args.dtree_module
print "classifier: ", args.classifier
print "attributes: ", args.attributes_file
print "training: ", args.training_file

# Train
training_data = dataset.DataSet(args.training_file, all_attributes)



# # testing the Node class
# child1 = Node(classifier)
# child2 = Node(classifier)
#
# root = Node(classifier)
# root.add_child(child1)
# root.add_child(child2)
#
# print "\nRoot\n", str(root)
# print "\nChild1\n", str(child1)
# print "\nChild2\n", str(child2)
#
# print '-'*50
# root.del_child(child1)
#
# print "\nRoot\n", str(root)
# print "\nChild1\n", str(child1)
# print "\nChild2\n", str(child2)
#
# print '-'*50
# root.del_child(child2)
#
# print "\nRoot\n", str(root)
# print "\nChild1\n", str(child1)
# print "\nChild2\n", str(child2)


