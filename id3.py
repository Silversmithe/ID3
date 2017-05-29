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
from attributes import Attribute


class Node(object):
    """Represents the nodes that make up the decision tree"""

    def __init__(self, classifier, data=dataset.DataSet(), parent=None, children=list()):
        """
        Creates a new node

        :param: data: (DataSet) the set of data associated with this node
        :param: classifier: (str) describe from which attribute are we classifying the information
        :param: parent: (Node) the reference to the node that self is attached to
        :param: children: ([Node, ...]) list of children nodes attached to self
        """
        assert(type(classifier) is Attribute)

        self.attribute = None
        self.classifier = classifier
        self.data = data
        if self.data is not None:
            if self.classifier is not None:
                self.entropy = self.data.entropy(classifier=self.classifier)
        else:
            self.entropy = None

        self.parent = None
        self.children = list()

        self.set_parent(new_parent=parent)

        for child in children:
            self.add_child(new_child=child)

    def set_parent(self, new_parent):
        """
        Set the parent of SELF, or replace the current parent with the new parent

        :param new_parent:
        :return:
        """
        if new_parent is not None:
            if self.parent is not None:
                # remove SELF from parent's children
                try:
                    self.parent.children.remove(self)
                except ValueError:
                    print "error: problem removing self from parent children list"

            # now set the parent of SELF to the new parent
            self.parent = new_parent
            self.parent.children.append(self)
        else:
            self.parent = new_parent

    def add_child(self, new_child):
        """
        Add a new child to the list of children for SELF
        :param new_child:
        :return:
        """
        assert(new_child is not None)
        if new_child not in self.children:
            new_child.set_parent(new_parent=self)

    def del_child(self, child):
        """
        Remove a child from the list of children in SELF

        :param child:
        :return:
        """
        assert(child is not None)
        try:
            child.set_parent(new_parent=None)
            self.children.remove(child)
        except ValueError:
            print "error: problem removing child from children list"

    def __str__(self):
        return "id: " + str(id(self)) + "\nclassifier: " + self.classifier.name + "\ndata-size: " + str(len(self.data)) + "\nparent: " + str(id(self.parent)) + "\nchildren: " + str(self.children)


class DTree(object):
    """Represents a decision tree created with the ID3 algorithm"""

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
        # initialize the beginning of the tree

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
        return ""


