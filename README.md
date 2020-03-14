# KBQA Saas and SimpliFi #


### Problem Statement

On Wall Street, the industry standard for financial data is the Bloomberg Terminal, which offers customers lots of in-depth data. However, it is expensive and hard to use, requiring a $24,000 annual subscription, a specialized keyboard, and lots of practice to master its keyboard commands and cluttered interface. 

With this project, we wanted to bring the benefit of using financial data to retail investors in a more familiar form - simply asking a question. Using a Bidirectional Attentive Memory Network (described in Core Model), we created SimpliFi, a tool with which users can simply ask for details about a company in natural language.

However, during the process of implementing SimpliFi, we realized that the process of building a knowledge base was complicated and very time-consuming, and that we had built the parsing, training and querying tools from scratch. We believe that both the creation and use of KBQA models ought to be made easy. Since we already had code that we used to build the knowledge base for SimpliFi, we decided to also create a service that automatically creates and trains a BAMnet model from a single simplified file input. 

### Core Model

Both SimpliFi and the KBQA SaaS use a Bidirectional Attentive Memory Network to answer questions. This model architecture significantly outperformed previous information-retrieval based methods while remaining competitive with (hand-crafted) semantic parsing based methods.

["Bidirectional Attentive Memory Networks for Question Answering over Knowledge Bases"](https://arxiv.org/abs/1903.02188)

#### System requirements

1. pip
2. npm
3. python3.6+

#### Options for training the model for use in Simplifi.

1. Train the model through the KBQA SaaS React frontend.

2. Download the pretrained model from Google Docs.


## KBQA SaaS

### Input and Output

Input: A dataset in the specified format. One will be provided in the root directory called result_spy.json which contains data from stocks in the $SPY ETF.

Ouput: A trained model that can be queried via the api endpoint. The same model will also be used for SimpliFi.
Ex: localhost:5000/answer?question=what_is_the_revenue_of_$appl_? 


### How to run (Docker)

W2V download for training takes about 7 minutes.

Build embeddings takes 6 minutes.

Training model takes about 13 minutes.



## SimpliFi

### Input and Output

Input: A question (string) containing a valid stock ticker (E.g, $aapl or $tsla)

Output: An answer (string) containing the requested detail about the company (revenue, industry, market cap, etc.)


<!-- ### Model & Data

You should put the model, embeddings, and data folder in kbqa-saas-flask/qa

Model: http://andrewacomb.me/bamnet.md

Pretrained W2V Embeddings: http://nlp.stanford.edu/data/wordvecs/glove.840B.300d.zip

Preprocessed Data: http://andrewacomb.me/data.zip -->


### How to run (Docker)

Docker Image: [docker image link]

Dockerfile: [dockerfile link]

#### Step 1. Clone and navigate to this repository

```
https://github.com/AndrewAcomb/KBQA-SaaS-SimpliFi.git
cd KBQA-SaaS-SimpliFi
```

#### Step 2. Download processed data and pretrained model

```
cd ks-flask/question-answering && { curl -O http://andrewacomb.me/data.zip ; curl -O http://andrewacomb.me/bamnet.md ; unzip data.zip ; rm data.zip ; cd -; }
```


#### Step 3. Build and run the SimpliFi Docker image

```
docker build -t simplifi .
docker run simplifi
```

#### Step 4. Open your browser and go to http://localhost:5000/




## Reference

Yu Chen, Lingfei Wu, Mohammed J. Zaki. **"Bidirectional Attentive Memory Networks for Question Answering over Knowledge Bases."** *In Proc. 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT2019). June 2019.*
