# ------------------------- Vocab2id Augmentation -------------------------
def add_topic_entity(vocab, topic_entity, index):
    """
    Description: 
    Parameters: 
    Return: 
    """
    topic_entity_lower = topic_entity.lower()

    if topic_entity_lower not in vocab:

        vocab[topic_entity_lower] = index = index + 1

    return (vocab, index)


def add_entity(vocab, entity, index):
    """
    Description: 
    Parameters: 
    Return: 
    """
    entity_words = entity.replace("-", " ").split(" ")
    for entity_word in entity_words:

        entity_word_lower = entity_word.lower()

        if entity_word_lower not in vocab:

            vocab[entity_word_lower] = index = index + 1

    return (vocab, index)


def augment_vocab(data, old_vocab):
    """
    Description: Adds new topic entities to vocab2id. Starts off from last index.
    Parameters: (Dict) Raw data from load functions, (Dict) Original vocab2id.
    Return: (Dict) Vocab2id augmented with new topic entities.
    """
    index = max(old_vocab.values())
    vocab = old_vocab

    for topic_entity, topic_entity_info in data.items():

        vocab, index = add_topic_entity(vocab, topic_entity, index)

        for entity in topic_entity_info.keys():

            vocab, index = add_entity(vocab, entity, index)

    return vocab
