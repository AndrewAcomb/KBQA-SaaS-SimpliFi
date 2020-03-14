from create_model import update_config, generate_embeddings, build_training_data, train_model
from question_answering import load_data, answer_question
from sys import argv

if __name__ == "__main__":

    if argv[1] == "update_config":
        update_config()
        print("Config updated")
    if argv[1] == "generate_embeddings":
        generate_embeddings('question-answering/config/bamnet_webq.yml','question-answering/glove.840B.300d.w2v')
        print("Embeddings generated")
    if argv[1] == "build_training_data":
        build_training_data('question-answering/config/bamnet_webq.yml')
        print("Training data built")
    if argv[1] == "train_model":
        train_model('question-answering/config/bamnet_webq.yml')
        print("Model trained")


