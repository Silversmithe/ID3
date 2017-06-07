"""
File:           dataset.py

Specifies an interface for storing individual datapoints (class Example), and collections
of datapoints (class DataSet). A DataSet can be initialized from a data file in the format
described in section 1.
"""
import math
import re
import sys
import math
import attributes


class Example:
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
    

class DataSet:
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

    def entropy(self, classifier):
        """
        1: completely random
        0: no randomness
        Attribute (overall)
        Classifier (the different values of an attribute?)

        Measure the randomness of a set with respect to a classifier
        *** Classifier must be a boolean classifier ***

        Determine the entropy of a collection with respect to a classifier.
        An entropy of zero indicates the collection is completely sorted.
        An entropy of one indicates the collection is evenly distributed with
        respect to the classifier.

        Entropy in bits for a variable with values v1, v2, ..., vk
        H(v) = - SUM[k](P(vk) * log_2(P(vk)))

        Entropy for a boolean variable
        B(q) = -(q log_2(q) + (1-q) * log_2(1-q))

        The sums of the entropys of the positive of the classifier and the negative of the classifier

        :param classifier:  (Attribute)
        :return:
        """
        h = 0

        if len(self) == 0:
            return 0

        size = len(self)
        for attr in classifier.values:
            # for each value in the classifier
            probability = float(len([x for x in self.all_examples if x.get_value(classifier.name) == attr]))/float(size)
            res = 0 if probability <= 0 else probability
            # print attr, ": ", probability
            h += probability * res

        return -1 * h

    def remainder(self, target_attr, attr):
        """

        :param target_attr:
        :param attr:
        :return:
        """
        total = 0
        for value in attr.values:
            # ENTROPY
            temp = DataSet()
            temp.all_examples = [x for x in self.all_examples if x.get_value(attr) == value]
            # WEIGHT
            num_pos = temp.total_positive(target_attr)
            val = num_pos + (len(temp)-num_pos)
            actual = self.total_positive(target_attr) + (self.__len__()-self.total_positive(target_attr))

            total += (float(val)/float(actual)) * temp.entropy(target_attr)

        return total

    def gain(self, target_attr, attr):
        """
        Information gain is the expected reduction in entropy

        Gain(A) = B (p/p+n) - Remainder(A)

        where :
        B * (p/p+n)
        is the entropy of a given set of examples with p positives and n negatives

        :return:
        """
        current_entropy = self.entropy(target_attr)
        # print
        # print attr

        gain = current_entropy - self.remainder(target_attr=target_attr, attr=attr)
        # print gain
        return gain

    def total_positive(self, classifier):
        """

        :param classifier:
        :return:
        """
        return len([x for x in self.all_examples if x.get_value(classifier) == 'yes'])

    def is_all_positive(self, classifier):
        """

        :param classifier:
        :return:
        """
        return self.total_positive(classifier) == len(self)

    def is_all_negative(self, classifier):
        """

        :param classifier:
        :return:
        """
        return (len(self) - self.total_positive(classifier)) == len(self)
