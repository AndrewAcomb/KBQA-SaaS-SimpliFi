import itertools


# ------------------------- KB Generation -------------------------
def initialize_node():
    """
    Description: Initializes empty knowledge base node.
    Parameters: None
    Return: (Dict) Dictionary representation of empty node.
    """
    node = {}
    node.update({'name': [],
                 'alias': [],
                 'notable_types': [],
                 'type': [],
                 'neighbors': {}})
    return node
    

def create_field_node(field, val):
    """
    Description: Creates field node containing information for one entity node to be appended to neighbors.
    Parameters: (str) Data field of entity, (str) Answer to data field. 
    Return: (Dict) Dictionary representation of filled field_node.
    """
    
    field_node = initialize_node()
    field_node['name'].append(val)
    
#     if "(" in field:
#         field_node['alias'].append(field.split(" (")[0])
    
    return field_node


def create_entity_node(entity_info):

    """
    Description: Creates entity node.
    Parameter: (Dict) Dictionary containing field and answer pairs.
    Output: (Dict) Dictionary representation of entity node.
    """

    entity_node = initialize_node()
    for field, val in entity_info.items():
        
        field_lower = field.lower()
        predicate = '/' + field_lower.replace(" ", "_")

        field_node = create_field_node(field, val)
        entity_node['neighbors'][predicate] = [{'/m/{}'.format(next(global_index)): field_node}]
    
    return entity_node


def create_knowledge_base(data):
    """
    Description: Creates knowledge base.
    Parameters: (Dict) Dictionary representation of raw data from load functions.
    Return: (Dict) Dictionary represntation of knowledge base.
    """

    knowledge_base = {}

    global global_index
    #Starting at 2 for entity2id creation
    global_index = itertools.count(2)

    for entity, info in data.items():

        entity_node = create_entity_node(info)
        knowledge_base[entity] = entity_node

    return knowledge_base
