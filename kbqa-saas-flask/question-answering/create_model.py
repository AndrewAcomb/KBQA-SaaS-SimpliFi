import question_answering as qa
from core.utils.generic_utils import dump_embeddings
from core.utils.utils import *
from core.build_data.build_data import build_vocab, build_data, build_seed_ent_data
from core.build_data import utils as build_utils
from core.bamnet.bamnet import BAMnetAgent
import yaml
import os
import timeit
import numpy as np


def update_config(config_path='question-answering/config/bamnet_webq.yml', new_data_dir=None, new_model=None):
    """
    Description: Update the config template file with the desired data directory
    Parameters: (String, String) Relative paths to data directory and config file
    """

    with open(config_path, "r") as setting:
        new_config = yaml.load(setting)

    data_dir = new_config['data_dir']

    entityType2id = load_json(os.path.join(data_dir, 'entityType2id.json'))
    relation2id = load_json(os.path.join(data_dir, 'relation2id.json'))
    vocab2id = load_json(os.path.join(data_dir, 'vocab2id.json'))
    
    new_config['vocab_size'] = len(vocab2id)
    new_config['num_ent_types'] = len(entityType2id)
    new_config['num_relations'] = len(relation2id)

    if new_data_dir:
        new_config['data_dir'] = new_data_dir
        new_config['pre_word2vec'] = new_data_dir + '/glove_pretrained_300d_w2v.npy'

    if new_model:
        new_config['model_file'] = new_model

    with open(config_path, 'w') as outfile:
       yaml.dump(new_config, outfile, default_style='double-quoted')



def generate_embeddings(config_path='question-answering/config/bamnet_webq.yml', glove="question-answering/glove.840B.300d.w2v"):
    """
    Description: Generate GLOVE word embedding vectors for the vocabulary
    Parameters: (String, String) Relative paths to config file and glove model
    Output: (.npy File) Creates file with word embedding vectors for BAMnet training
    """
    with open(config_path, "r") as setting:
        config = yaml.load(setting)
    

    data_dir = config['data_dir']
    emb_size = config['vocab_embed_size']
    vocab_dict = load_json(os.path.join(data_dir, 'vocab2id.json'))

    out_path = config['pre_word2vec']


    dump_embeddings(vocab_dict, glove, out_path, emb_size=emb_size, binary=False)


def build_training_data(config_path='question-answering/config/bamnet_webq.yml'):
    """
    Description: Create train/valid/test questions into vectors for BAMnet training
    Parameters: (String) Relative path to config file
    Output: (3 .json Files) train_vec.json, valid_vec.json, test_vec.json in /data
    """

    with open(config_path, "r") as setting:
        config = yaml.load(setting)

    data_dir = config['data_dir']

    # Load in training data
    train_data = load_ndjson(os.path.join(data_dir, 'raw_train.json'))
    valid_data = load_ndjson(os.path.join(data_dir, 'raw_valid.json'))
    test_data = valid_data[:(len(valid_data)//3)]

    freebase = load_ndjson(os.path.join(data_dir, 'freebase_full.json'), return_type='dict')

    # Load in ID mappings
    entity2id = load_json(os.path.join(data_dir, 'entity2id.json'))
    entityType2id = load_json(os.path.join(data_dir, 'entityType2id.json'))
    relation2id = load_json(os.path.join(data_dir, 'relation2id.json'))
    vocab2id = load_json(os.path.join(data_dir, 'vocab2id.json'))

    # Build data
    train_vec = build_data(train_data, freebase, entity2id, entityType2id, relation2id, vocab2id)
    valid_vec = build_data(valid_data, freebase, entity2id, entityType2id, relation2id, vocab2id)
    test_vec = build_data(test_data, freebase, entity2id, entityType2id, relation2id, vocab2id)
    dump_json(train_vec, os.path.join(data_dir, 'train_vec.json'))
    dump_json(valid_vec, os.path.join(data_dir, 'valid_vec.json'))
    dump_json(test_vec, os.path.join(data_dir, 'test_vec.json'))



def train_model(config_path='question-answering/config/bamnet_webq.yml'):
    """
    Description: Train a BAMnet model with knowledge base and questions in /data
    Parameters: (String) Relative path to config file
    Output: (1 .md File) BAMnet model weights. Use for question_answering.py
    """

    # build_utils.vectorize_data()

    with open(config_path, "r") as setting:
        opt = yaml.load(setting)
    
    # Load data
    train_vec = load_json(os.path.join(opt['data_dir'], opt['train_data']))
    valid_vec = load_json(os.path.join(opt['data_dir'], opt['valid_data']))

    vocab2id = load_json(os.path.join(opt['data_dir'], 'vocab2id.json'))

    ctx_stopwords = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
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


    # Vectorize data
    train_queries, train_raw_queries, train_query_mentions, train_memories, _, train_gold_ans_inds, _ = train_vec
    train_queries, train_query_words, train_query_lengths, train_memories = build_utils.vectorize_data(train_queries, train_query_mentions, \
                                        train_memories, max_query_size=opt['query_size'], \
                                        max_query_markup_size=opt['query_markup_size'], \
                                        max_mem_size=opt['mem_size'], \
                                        max_ans_bow_size=opt['ans_bow_size'], \
                                        max_ans_path_bow_size=opt['ans_path_bow_size'], \
                                        vocab2id=vocab2id)

    valid_queries, valid_raw_queries, valid_query_mentions, valid_memories, valid_cand_labels, valid_gold_ans_inds, valid_gold_ans_labels = valid_vec
    valid_queries, valid_query_words, valid_query_lengths, valid_memories = build_utils.vectorize_data(valid_queries, valid_query_mentions, \
                                        valid_memories, max_query_size=opt['query_size'], \
                                        max_query_markup_size=opt['query_markup_size'], \
                                        max_mem_size=opt['mem_size'], \
                                        max_ans_bow_size=opt['ans_bow_size'], \
                                        max_ans_path_bow_size=opt['ans_path_bow_size'], \
                                        vocab2id=vocab2id)

    start = timeit.default_timer()

    model = BAMnetAgent(opt, ctx_stopwords, vocab2id)
    model.train([train_memories, train_queries, train_query_words, train_raw_queries, train_query_mentions, train_query_lengths], train_gold_ans_inds, \
        [valid_memories, valid_queries, valid_query_words, valid_raw_queries, valid_query_mentions, valid_query_lengths], \
        valid_gold_ans_inds, valid_cand_labels, valid_gold_ans_labels)

    print('Runtime: %ss' % (timeit.default_timer() - start))
