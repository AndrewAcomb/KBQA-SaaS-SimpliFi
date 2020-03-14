from functools import reduce

# ------------------------- Entity2id Generation -------------------------


def count_fields(data):
    """
    Description: Counts the number of fields in data.
    Parameters: (Dict) Dictionary of raw data from load functions.
    Return: Number of fields in data.
    """
    num_fields = reduce(lambda
                        field_count,
                        field_list: field_count + len(field_list),
                        data.values(), 0)

    return num_fields


def generate_entity2id(data):
    """
    Description: Generate entity2id word embeddings. The entity refers to "field" in this codebase.
    Parameters: (Dict) Dictionary representation of raw data from load functions.
    Return: (Dict) Dictionary representation of entity2id.
    """

    num_fields = count_fields(data)
    default_entity2id = {"PAD": 0, "UNK": 1}
    additional_entity2id = {"/m/{}".format(i): i for i in range(2, num_fields + 2)}
    default_entity2id.update(additional_entity2id)
    return default_entity2id
