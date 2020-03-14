import sys
import os
import string
import yaml
from core.bamnet.bamnet import BAMnetAgent
from core.utils.utils import get_config, load_json, load_ndjson
from core.build_data.build_data import build_vocab, build_data, build_seed_ent_data, build_ans_cands
from core.build_data.utils import vectorize_data


# --------- Load Knowledge Base, Existing Model, ID Mappings ------------

def load_data(cfg = 'question-answering/config/bamnet_webq.yml'):
    """
    Description: Load config settings, knowledge base, and ID mappings into memory
    Parameters: (String) Path to configuration file
    Output: (Dict) Dictionary containing token mappings
    """

    data = {}
    
    # Fetch BAMnet configuration settings 
    with open(cfg, "r") as setting:
        data['opt']  = yaml.load(setting)
    
    # Load token mappings
    data['entity2id'] = load_json(os.path.join(data['opt']['data_dir'], 'entity2id.json'))
    data['entityType2id'] = load_json(os.path.join(data['opt']['data_dir'], 'entityType2id.json'))
    data['relation2id'] = load_json(os.path.join(data['opt']['data_dir'], 'relation2id.json'))
    data['vocab2id'] = load_json(os.path.join(data['opt']['data_dir'], 'vocab2id.json'))
    
    # Load context stopwords
    data['ctx_stopwords'] = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
     "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
     'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their',
     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
     'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
     'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
     'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
     'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
     'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
     'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 
     'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', 
     "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 
     'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 
     'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
    
    # Load knowledge base
    data['kb'] = load_ndjson(os.path.join(data['opt']['data_dir'], 'freebase_full.json'), return_type='dict')
    
    return(data)


def load_model(data):
    """
    Description: Load model into memory
    Parameters: (Dict) Data from load_data()
    Output: (BAMnetAgent) Trained BAMnet model from memory
    """

    model = BAMnetAgent(data['opt'], data['ctx_stopwords'], data['vocab2id'])
    return(model)



# ---------------------------- Parse Query -----------------------------

def get_kb_key(q):
    """
    Description: Get the knowledge base key from a query with a stock ticker
    Parameters: (String) Query as entered by the user
    Output: (String) knowledge base key 
    """

    assert ('$' in q), "Query must contain a valid ticker."
    return(((q.replace('?','').split('$'))[1].split()[0]).upper())


def parse_query(q, data):
    """
    Description: Get the knowledge base key from a query with a stock ticker
    Parameters: (String) Query as entered by the user, (Dict) data from load_data() output
    Output: (Array) Array containing inputs to model.predict, (Array) Labels for potential answers
    """

    #  Remove punctuation, lowercase, split on spaces
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    raw_query = ((q.translate(translator)).lower()).split()

    # Get kb_key
    kb_key = get_kb_key(q)

    # Ensure raw_query is at most 13 words
    if len(raw_query) > 13:
        raw_query = raw_query[:13]
    
    # Tokenize Query
    query = [data['vocab2id'][word] if word in data['vocab2id'] else 1 for word in raw_query]
    query.extend([0 for _ in range(13 - len(raw_query))])
    query = [query]
    
    # Memory & Candidate Answer Labels
    ans_cands = build_ans_cands(data['kb'][kb_key], 
                                            data['entity2id'], \
                                            data['entityType2id'], 
                                            data['relation2id'], 
                                            data['vocab2id'])
    memory = [ans_cands[:-1]]
    cand_labels = [ans_cands[-1]]
        
    # Vectorize Data
    query, query_words, _, memory = vectorize_data(query, [[]], memory, \
                                            max_query_size=data['opt']['query_size'], \
                                            max_query_markup_size=data['opt']['query_markup_size'], \
                                            max_ans_bow_size=data['opt']['ans_bow_size'], \
                                            vocab2id=data['vocab2id'])
    
    return([memory, query, query_words, [raw_query], [[]], [len(raw_query)]], cand_labels)   

    
# ---------------------------- Answer Query -----------------------------

def answer_question(q):
    """
    Description: Answer given question. Must load in model and data each time it is called.
    Parameters: (String) A question with a valid ticker
    Output: (String) The model's answer to the given question
    """
    
    data = load_data()
    model = load_model(data)

    inputs, possible_answers = parse_query(q, data)
    answer = model.predict(inputs, possible_answers)

    return(answer[0][0][0])


def answer_question_quick(q, model, data):
    """
    Description: Answer given question using given model and data from load_data()
    Parameters: (String) question, (BAMnetAgent) pretrained BAMnet model, (Dict) data from load_data()
    Output: (String) The model's answer to the given question
    """

    inputs, possible_answers = parse_query(q, data)
    answer = model.predict(inputs, possible_answers)

    return(answer[0][0])

