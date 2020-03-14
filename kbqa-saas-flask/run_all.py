from sys import argv

from qa.create_model import update_config, generate_embeddings, build_training_data, train_model
from qa.question_answering import load_data, answer_question


if __name__ == "__main__":

    if argv[1] == "update_config":
        update_config()
        print("Config updated")
    if argv[1] == "generate_embeddings":
        generate_embeddings()
        print("Embeddings generated")
    if argv[1] == "build_training_data":
        build_training_data()
        print("Training data built")
    if argv[1] == "train_model":
        train_model()
        print("Model trained")


