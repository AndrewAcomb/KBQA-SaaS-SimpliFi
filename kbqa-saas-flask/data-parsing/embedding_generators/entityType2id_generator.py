def generate_entityType2id(data):
    """
    """

    default_entityType2id = {"PAD": 0, "UNK": 1}
    field_set = set(sum([list(field_info.keys())
                         for field_info in data.values()],
                    []))

    additional_entityType2id = {"/m/{}".format(field.lower().replace(' ', '_')): i 
                                for i, field in enumerate(field_set, 2)}
    default_entityType2id.update(additional_entityType2id)

    return default_entityType2id

