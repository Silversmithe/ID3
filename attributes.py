import re
import sys

class Attribute:
  'A single attribute description: name + permissible values'

  def __init__(self, name, values):
    self.name = name
    self.values = values

  def __str__(self):
    return self.name + ' --> ' + str(self.values)


class Attributes:
  'An ordered collection of attributes and values'

  # Create a new instance of an attribute collection. If a file is
  # specified, use it to initialize the collection from that file.
  # The expected file format is:
  # attr-name:value[,value]...
  def __init__(self, attribute_file=False):
    self.attributes = []
    if attribute_file:
      line_num = 1
      for next_line in attribute_file:
        valid_line = re.match("^(.*[^ ]+)\s*:\s*(\S*)\s*$", next_line)
        if not valid_line:
          sys.stderr.write("%s: %d: Failed to parse\n" %
                           (attribute_file.name, line_num))
          sys.exit(1)
        name = valid_line.group(1)
        values = valid_line.group(2).split(',')
        new_attr = Attribute(name, values)
        self.attributes.append(new_attr)
        line_num += 1

  # Implement the [] operator. If an index is specified, return the
  # corresponding attribute. This is useful for correlating an attribute
  # to a value from an example, where we don't know the attribute's
  # name, but we have the order from the example. A string can also
  # be used as an index to retrieve the attribute with the specified
  # name.
  def __getitem__(self, key):
    if isinstance(key, int):
      return self.attributes[key]
    elif isinstance(key, str):
      for attr in self.attributes:
        if attr.name == key:
          return attr
      sys.stderr.write("Erroneous call to __getitem__\n")
      sys.exit(1)

  def __len__(self):
    return len(self.attributes)

  def __str__(self):
    result = '[\n'
    for attr in self.attributes:
      result += ('  ' + str(attr) + '\n')
    result += ']'
    return result

  def __copy__(self):
    new_instance = Attributes()
    new_instance.attributes = self.attributes[:]
    return new_instance

  def all_names(self):
    return [attr.name for attr in self.attributes]

  # If the key is a name, remove the attribute(s) with that name. If the
  # key is an attribute, remove that attribute.
  def remove(self, key):
    if isinstance(key, str):
      for attr in self.attributes:
        if attr.name == key:
          self.attributes.remove(attr)
    else:
      self.attributes.remove(key)

