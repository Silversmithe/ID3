"""
File:           id3.py

Author:         Alexander Adranly

Description:

ID3 Construction:
Recursively split until:
- all examples are the same classification, or
- we have no more features to split on, or
- we have no more examples

Split according to the feature that does the best job dividing the examples by
classification (Entropy)
"""

import copy
import dataset
from node import Node
from attributes import Attribute
import math


class DTree:
    """Represents a decision tree created with the ID3 algorithm"""

    """
    ID3 Pseudocode

    ID3 (Exampels, Target_Attribute, Attributes)
        create a root node for the tree

        if all examples are positive, return the single-node tree Root, with label = +
        if all examples are negative, return the single-node tree root, with label = -

        if number of predicting attributes is empty, then return the single node tree root with,
            \ label = most common value of the target attribute in the examples

        Otherwise Begin

            A <- The attribute that best classifies examples
            Decision tree attribute for Root = A
            For each possible value, vi, of A,
                Add a new tree branch below Root, corresponding to the test A = vi
                let examples(vi) be the subset of examples that have the value vi for A
                if examples(vi) is empty)
                    then below this new branch add a leaf node with label = most common target value
                        \ in the examples
                else below this new branch add the subtree ID3 (examples(vi), Target_attribute, attributes - {A})

        End
        Return Root
    """

    def __init__(self, classifier, training_data, attributes):
        """
        Creates a new decision tree

        :param classifier: (Attribute) Attribute that is being used for classification
        :param training_data: (DataSet) Set of training data
        :param attributes: (Attributes) All attributes in this domain
        """
        self.classifier = classifier
        self.training_data = training_data
        self.attributes = attributes
        self.attributes.remove(self.classifier)  # remove the classifier because we do not need to split on it

        # initialize the beginning of the tree
        root = Node(data=self.training_data, parent=None, children=list(), attribute=None)
        self.id3(root=root, target_attr=self.classifier, attrs=self.attributes, indent=0)
        self.decision_tree = root
        # self.checksum(self.decision_tree)

    def test(self, classifier, testing_data):
        """
        Uses a decision tree to classify test examples

        :param classifier: (Attribute) Attribute that is being used for classification
        :param testing_data: (DataSet) Set of testing data
        :return: (int) Number of test examples that were correctly classified by the decision tree
        """
        return 0

    def dump(self):
        """
        Prints out a visual representation of the decision tree
        """
        self.pre_order(self.decision_tree, 0)

        return ""

    def pre_order(self, node, indent):
        """

        :param node:
        :return:
        """
        if node.attribute.name in ['yes', 'no', '--']:
            print ' ' * indent, '<' + node.attribute.name + '>'
            return
        else:
            for child in node.children:
                print ' ' * indent, node.attribute.name, ":", child[0]
                # print ' ' * indent, '(', len(node.data_set), ')'
                self.pre_order(child[1], indent + 1)

    # HELPER FUNCTIONS
    def id3(self, root, target_attr, attrs, indent):
        """

        :param root:
        :param target_attr:
        :param attrs:
        :param indent:
        :return:
        """
        # pass in root
        # check if all examples are positive, then return a ('yes')
        if root.data_set.is_all_positive(classifier=target_attr):
            print ' ' * indent, 'assigned yes'
            root.attribute = Attribute('yes', 'end')
            return

        # check if all examples are negative, then return a ('no')
        if root.data_set.is_all_negative(classifier=target_attr):
            print ' ' * indent, 'assigned no'
            root.attribute = Attribute('no', 'end')
            return

        # there are attributes to split upon
        # decide the split based on gain

        if len(attrs) > 0:
            # START: BEST ATTRIBUTE
            best_attributes = []
            top_attr = None

            # find the best attribute
            for attr in attrs:
                # iterate through each value in the attribute
                gain = root.data_set.gain(target_attr, attr)

                if top_attr is None:
                    top_attr = (attr, gain)
                elif top_attr[1] == gain:
                    best_attributes.append((attr, gain))
                elif top_attr[1] < gain:
                    top_attr = (attr, gain)

            best_attributes.append(top_attr)

            # organize alphabetically
            # "Also, if there is a tie in entropy reduction between multiple attributes, you should choose the attribute
            # whose name is earlies in the alphabet (using Python's native string comparison)
            def name(elem):
                return elem[0].name

            # sort based on name
            best_attributes.sort(key=name)

            # BUILD CHILDREN
            # create the attribute for this node
            root.attribute = best_attributes[0][0]

            print ' ' * indent, "best attribute: ", root.attribute.name

            root.attribute.values.sort()

            # END: BEST ATTRIBUTES
            print ' ' * indent, root.attribute.name.upper()
            print ' ' * indent, 'number positive examples: ', root.data_set.total_positive(target_attr)
            print ' ' * indent, 'total examples: ', len(root.data_set)
            # ADD CHILDREN

            for value in root.attribute.values:
                print '\n', '  ' * indent, root.attribute.name.upper(), ": ", value.upper()

                example_set = [x for x in root.data_set.all_examples if x.get_value(root.attribute) == value]

                # examples to work with
                # make new node to pass down
                next_node = Node(data=dataset.DataSet(), parent=root, children=list(), attribute=None)

                attributes = copy.copy(attrs)
                attributes.remove(root.attribute)

                if len(example_set) == 0:
                    print ' ' * indent, "warning: no examples"
                    # choose the most prevalent example from the population that falls into the parent's domain
                    parent = root
                    while parent is not None:

                        positive_population = float(parent.data_set.total_positive(target_attr))
                        half_size = float(float(len(parent.data_set)) / 2.0)
                        print ' ' * indent, parent.attribute
                        for ex in parent.data_set.all_examples:
                            print ex.values

                        print '-' * 50, '\n(', positive_population, ", ", half_size, ")\n", '-' * 50
                        print

                        if positive_population > half_size:
                            # choose the positive examples
                            print ' ' * (indent + 1), "warning: assign positive"
                            next_node.attribute = Attribute('yes', 'end')
                            break
                        elif positive_population < half_size:
                            # choose the negative examples
                            print ' ' * (indent + 1), "warning: assign negative"
                            next_node.attribute = Attribute('no', 'end')
                            break
                        else:
                            parent = parent.parent
                    else:
                        # finishes the loop correctly
                        # at the parent node
                        # SUSPICIOUS
                        root.attribute = Attribute(target_attr.values.sort()[0], 'end')

                    # no need to delve any more into next node

                    root.children.append((value, next_node))
                    continue

                # make a dataset with all the value-specific information and store in next node
                next_node.data_set.all_examples = example_set

                # update the children of the node by recursing through
                self.id3(root=next_node, target_attr=target_attr, attrs=attributes, indent=indent + 1)

                root.children.append((value, next_node))

        else:
            # RUN OUT OF FEATURES
            # no attributes
            num_pos = root.data_set.total_positive(target_attr)
            num_neg = len(root.data_set) - num_pos
            tie = num_pos == num_neg
            print ' ' * indent, "warning: out of attributes"

            if tie:
                print ' ' * indent, "tie"
                # this is what we do in the event of a tie:
                current_parent = root.parent

                while current_parent.parent is not None:
                    num_pos = current_parent.data_set.total_positive(target_attr)
                    num_neg = len(current_parent.data_set) - num_pos
                    tie = num_pos == num_neg

                    if not tie:
                        root.attribute = Attribute('yes', 'end') if num_pos > num_neg else Attribute('no', 'end')
                        print ' ' * indent, "\twarning: assigned ", root.attribute.name
                        break
                    else:
                        current_parent = current_parent.parent

                else:
                    # gets to the actual root node
                    # finishes the loop correctly
                    # at the parent node
                    # choose earliest value
                    root.attribute = Attribute(target_attr.values.sort()[0], 'end')
            else:
                print ' ' * indent, "not tie"
                # in the event of NOT a tie
                root.attribute = Attribute('yes', 'end') if num_pos > num_neg else Attribute('no', 'end')
                print ' ' * indent, "\twarning: assigned ", root.attribute.name
