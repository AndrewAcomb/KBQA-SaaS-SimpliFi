# ------------------------- Relation2id Generation -------------------------
def get_unique_relations(data):

    #relations are predicates
    relations = set()
    for info in data.values():
        
        for field in info.keys():
            
            field_lower = field.lower()
            predicate = '/' + field_lower.replace(" ", "_")
            relations.add(predicate)

    return list(relations)


def generate_relation2id(data):

    unique_relations = get_unique_relations(data)
    default = {"PAD": 0, "UNK": 1}
    num_relations = len(unique_relations)
    additional = {predicate: i for i, predicate in enumerate(unique_relations, start = 2)}
    default.update(additional)
    return default
