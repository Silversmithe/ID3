"""
File:           dataset.py

Specifies an interface for storing individual datapoints (class Example), and collections
of datapoints (class DataSet). A DataSet can be initialized from a data file in the format
described in section 1.
"""
import math
import re
import sys


class Example(object):
    """An individual example with values for each attribute"""

    def __init__(self, values, attributes, filename, line_num):
        if len(values) != len(attributes):
          sys.stderr.write(
            "%s: %d: Incorrect number of attributes (saw %d, expected %d)\n" %
            (filename, line_num, len(values), len(attributes)))
          sys.exit(1)
        # Add values, Verifying that they are in the known domains for each
        # attribute
        self.values = {}
        for ndx in range(len(attributes)):
            value = values[ndx]
            attr = attributes.attributes[ndx]
            if value not in attr.values:
                sys.stderr.write("%s: %d: Value %s not in known values %s for attribute %s\n" %
                                 (filename, line_num, value, attr.values, attr.name))
                sys.exit(1)
            self.values[attr.name] = value

    # Find a value for the specified attribute, which may be specified as
    # an Attribute instance, or an attribute name.
    def get_value(self, attr):
        if isinstance(attr, str):
            return self.values[attr]
        else:
            return self.values[attr.name]
    

class DataSet(object):
    """A collection of instances, each representing data and values"""

    def __init__(self, data_file=False, attributes=False):
        self.all_examples = []
        if data_file:
            line_num = 1
            num_attrs = len(attributes)
            for next_line in data_file:
                next_line = next_line.rstrip()
                next_line = re.sub(".*:(.*)$", "\\1", next_line)
                attr_values = next_line.split(',')
                new_example = Example(attr_values, attributes, data_file.name, line_num)
                self.all_examples.append(new_example)
                line_num += 1

    def __len__(self):
        return len(self.all_examples)

    def __getitem__(self, key):
        return self.all_examples[key]

    def append(self, example):
        self.all_examples.append(example)

    # Determine the entropy of a collection with respect to a classifier.
    # An entropy of zero indicates the collection is completely sorted.
    # An entropy of one indicates the collection is evenly distributed with
    # respect to the classifier.
    def entropy(self, classifier):
        # IMPLEMENT ME!!!
        return 0.5
