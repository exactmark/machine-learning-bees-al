import xml.etree.ElementTree as ET


def read_data(xml_path):
    tree = ET.parse(xml_path)
    return tree.getroot()


def get_first_attribute_from_xml(node, target_attrib):
    pass


def get_network_data(xml_path):
    xml_root_node = read_data(xml_path)
    node_list = []
    for single_node in xml_root_node.iter('node'):
        node_list.append(single_node)
    from collections import namedtuple

    Place_Node = namedtuple('Place_Node', 'id x y')
    tuple_list = []
    for single_node in node_list:
        id = single_node.attrib['id']
        for sub_node in single_node:
            if sub_node.tag == 'cx':
                x = float(sub_node.text)
            elif sub_node.tag == 'cy':
                y = float(sub_node.text)
            else:
                raise KeyError
        tuple_list.append(Place_Node(id, x, y))

    return tuple_list
