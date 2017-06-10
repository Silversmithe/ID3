"""
File:           dataset.py

Specifies an interface for storing individual datapoints (class Example), and collections
of datapoints (class DataSet). A DataSet can be initialized from a data file in the format
described in section 1.
"""
import re
import sys
from math import log


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
        SHANNON'S ENTROPY

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
        :return: (entropy, dominant_value)

        entropy:
        dominant_value:
            None: if there are no examples
        """
        h = 0.0
        # dominant_value = (value, size)
        dominant_value = None

        if len(self.all_examples) == 0.0:
            # if there are no examples then all the examples are the same
            # there is order of nothingness
            # print 'no examples'
            return 0.0, None

        population_size = float(len(self.all_examples))

        # otherwise calculate entropy
        for value in classifier.values:
            # go through each value in the classifier
            # calculate the parts associated with that value
            # add it to the entropy sum
            partial_population = [x for x in self.all_examples if x.get_value(classifier.name) == value]

            if len(partial_population) == 0.0:
                # if this is zero, we just classify it as zero and move on
                # if there are examples and none of them are in this value, there is no way this value
                #       can be the most dominant
                h += 0.0
                continue
            else:
                # calculation of the partial probability
                partial_probability = float(float(len(partial_population))/population_size)
                partial_entropy = partial_probability * log(partial_probability, 2)
                h += partial_entropy

            # update the dominant value
            if dominant_value is None:
                # if the dominant value has not been initialized yet
                # collect the first value and add it to the dominant value
                dominant_value = value, len(partial_population)
            else:
                # if there is a new value with a partial population larger than the current dominant value
                # make this new value the dominant value
                if len(partial_population) > dominant_value[1]:
                    dominant_value = value, len(partial_population)

        return -1 * h, dominant_value[0]

    def remainder(self, target_attr, attr):
        """
        Calculated the remainder the data set given a certain attribute

        :param target_attr: (Attribute) The attribute to classify the nodes on
        :param attr: (Attribute) The specific attribute
        :return:
        (int) the remainder based on the attribute
        """
        total = 0
        for value in attr.values:
            # ENTROPY
            temp = DataSet()
            temp.all_examples = [x for x in self.all_examples if x.get_value(attr) == value]
            # WEIGHT
            num_pos = temp.partial_count(target_attr)
            val = num_pos + (len(temp)-num_pos)
            actual = self.partial_count(target_attr) + (self.__len__() - self.partial_count(target_attr))

            total += (float(val)/float(actual)) * temp.entropy(target_attr)[0]

        return total

    def gain(self, target_attr, attr, debug=False):
        """
        Information gain is the expected reduction in entropy

        Gain(A) = B (p/p+n) - Remainder(A)

        where :
        B * (p/p+n)
        is the entropy of a given set of examples with p positives and n negatives

        :param target_attr: (Attribute) attribute to classify based on
        :param attr: (Attribute)
        :param debug: (Boolean) Enable or disable debug messages
        :return:
        (int) the gain
        """
        current_entropy = self.entropy(target_attr)[0]
        # print
        # print attr

        gain = current_entropy - self.remainder(target_attr=target_attr, attr=attr)
        if debug is True:
            print attr, ": ", gain
        return gain

    def partial_count(self, classifier):
        """

        :param classifier: (Attribute): The attribute to classify the examples
        :return:
        (float): number of times that one of the classifier's arbitrary values appears in the dataset
        """
        classifier.values.sort()
        value = classifier.values[0]
        partial_set = [x for x in self.all_examples if x.get_value(classifier) == value]
        return float(len(partial_set))
