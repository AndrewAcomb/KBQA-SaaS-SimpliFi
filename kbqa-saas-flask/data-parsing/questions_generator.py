import random
from pprint import pprint

# ------------------------- Question Generation -------------------------


def generate_question(entity, field, answer):
    """
    Description: Generates single "what" question.
    Parameters: (str) Topic entity, (str) Field to ask about, (str) Answer to questions.
    Output: (str, str, str) Tuple containing (question, answer, entity)
    """
    return ("What is the {} of ${}?".format(field, entity), answer, entity)


def generate_questions(data):   
    """
    Description: Generates list of raw questions, answers, and entity topics.
    Parameters: (Dict) Dictionary containing data in specified format.
    Output: (List) List containing raw questions in (question, answer, entity) format.
    """
    raw_questions = []

    for entity, info in data.items():

        for field, answer in info.items():

            raw_questions.append(generate_question(entity, field, answer))

    return raw_questions


# ------------------------- Question Decoration -------------------------


def decorate_question(question, answer, entity, id):
    """
    Description: Takes raw question output and returns valid question format.
    Parameters: (str) Question text, (str) Question answer, (str) Topic entity, (str) Unique question id.
    Output: (Dict) Dictionary representation of valid question format.
    """

    decorated_question = {'answers': [answer],
                          'entities': [[entity, "ORGANIZATIONS"]],
                          'qText': question,
                          'qId': str(id),
                          'freebaseKey': entity,
                          'freebaseKeyCands': [entity],
                          'dep_path': []}

    return decorated_question


def decorate_questions(raw_questions):
    """
    Description: Iterates through raw question set and returns decorated question set.
    Parameters: (List) List of questions in (question, answer, entity) format.
    Output: (List) List of decorated question in format specified by Bamnet model.
    """
    decorated_questions = []

    for index, (question, answer, entity) in enumerate(raw_questions):

        decorated_questions.append(decorate_question(question, answer, entity, index))
    
    return decorated_questions


# ------------------------- Question Set Splitting -------------------------
def split_train_valid_set(questions):
    """
    Description: Splits question set into 80% training size and 20% validation size.
    Parameters: (List) List containing all questions.
    Output: (List, List) Tuple containing (training question set, validation question set).
    """
    random_questions = random.sample(questions, len(questions))
    validation_size = len(questions) // 5
    training_set, validation_set = random_questions[validation_size:], random_questions[:validation_size]
    
    return (training_set, validation_set)


# ------------------------- Question Pipeline -------------------------
def generate_question_sets(data):
    """
    Description: Takes in data and return question training and validation set in specified format.
    Parameters: (Dict) Dictionary representation of raw data from load functions.
    Output: (List, List) Tuple containing (question training set, question validation set).
    """
    raw_questions = generate_questions(data)
    decorated_questions = decorate_questions(raw_questions)

    train_set, valid_set = split_train_valid_set(decorated_questions)

    return (train_set, valid_set)