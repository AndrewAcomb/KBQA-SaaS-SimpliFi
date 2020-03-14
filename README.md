# KBQA Saas and SimpliFi #


### Problem Statement

On Wall Street, the industry standard for financial data is the Bloomberg Terminal, which offers customers lots of in-depth data. However, it is expensive and hard to use, requiring a $24,000 annual subscription, a specialized keyboard, and lots of practice to master its keyboard commands and cluttered interface. 

With this project, we wanted to bring the benefit of using financial data to retail investors in a more familiar form - simply asking a question. Using a Bidirectional Attentive Memory Network (described in Core Model), we created SimpliFi, a tool with which users can simply ask for details about a company in natural language.

However, during the process of implementing SimpliFi, we realized that the process of building a knowledge base was complicated and very time-consuming, and that we had built the parsing, training and querying tools from scratch. We believe that both the creation and use of KBQA models ought to be made easy. Since we already had code that we used to build the knowledge base for SimpliFi, we decided to also create a service that automatically creates and trains a BAMnet model from a single simplified file input. 

### Core Model

Both SimpliFi and the KBQA SaaS use a Bidirectional Attentive Memory Network to answer questions. This model architecture significantly outperformed previous information-retrieval based methods while remaining competitive with (hand-crafted) semantic parsing based methods.

[Bidirectional Attentive Memory Networks for Question Answering over Knowledge Bases](https://arxiv.org/abs/1903.02188)

#### System requirements

1. pip
2. npm
3. python3.6+
4. wget (cli tool to download large files)
5. docker

#### Options for training the model for use in Simplifi

1. Train the model through the KBQA SaaS React frontend

2. Download the built data and pretrained model (see running SimpliFi Step 2)




## KBQA SaaS

### Input and Output

Input: A dataset in the specified format. One will be provided in the root directory called result_spy.json which contains data from stocks in the $SPY ETF.

Ouput: A trained model that can be queried via the api endpoint. The same model will also be used for SimpliFi.
Ex: localhost:5000/answer?question=what_is_the_revenue_of_$appl_? 


### How to run (Docker)

Docker Image: [View]()

Dockerfile: [View]()

If you run the two lines below, skip to Step 4
```
docker pull aca7964/simplifi:initialcommit
docker run aca7964/simplifi:initialcommit
```

#### Step 1. Clone and navigate to this repository

```
https://github.com/AndrewAcomb/KBQA-SaaS-SimpliFi.git
cd KBQA-SaaS-SimpliFi
```

#### Step 2. Download Word2Vec embeddings

```
cd kbqa-saas-flask/qa&& { wget --no-check-certificate -r 'https://drive.google.com/uc?id=1DVouJLo_K5cs4iVjNlkF5Ed9NlsP9G9G&export=download' -O glove.840B.300d.w2v.zip; unzip glove.840B.300d.w2v.zip; rm glove.840B.300d.w2v.zip ; cd -; }
```

The download should take about 4 - 6 minutes.

#### Step 3. Build and run the KBQA SaaS Docker image, then

```
docker build -t kbqa .
docker run -d -p 5000:5000 kbqa
```

#### Step 4. Install npm modules, and start react

In a new CLI window, navigate back to this repository.
```
cd kbqa-saas-react && { npm install ; npm start; }
```

#### Step 5. Go to http://localhost:3000/, click 'Select File', select the starter data, and click 'Start Upload'

Starter Data: result_spy.json in root directory.

#### Step 6. Wait for model to train

Reformatting the Word2Vec embeddings to the data takes about 10 minutes.

Training the model takes about 15 minutes.

#### Step 7. Query the newly exposed API endpoint

The model you just trained is now availible to be queried at the given address.
Enter your question as a url in the following format: localhost:5000/answer?question=what_is_the_revenue_of_$aapl_? 




## SimpliFi

### Input and Output

Input: A question containing a valid stock ticker (Ex: What is the number of employees $AAPL has?)

Output: An answer containing the requested detail about the company (revenue, industry, market cap, etc.)


### How to run (Docker)

Docker Image: [View](https://hub.docker.com/r/aca7964/simplifi)

Dockerfile: [View](https://github.com/AndrewAcomb/KBQA-SaaS-SimpliFi/blob/master/Dockerfile)

If you run the two lines below, skip to Step 4
```
docker pull aca7964/simplifi:initialcommit
docker run -p 5000:5000  aca7964/simplifi:initialcommit
```

#### Step 1. Clone and navigate to this repository

```
git clone https://github.com/AndrewAcomb/KBQA-SaaS-SimpliFi.git
cd KBQA-SaaS-SimpliFi
```

#### Step 2. Download processed data and pretrained model

```
cd kbqa-saas-flask/qa && { curl -O http://andrewacomb.me/data.zip ; curl -O http://andrewacomb.me/bamnet.md ; unzip data.zip ; rm data.zip ; cd -; }
```

#### Step 3. Build and run the SimpliFi Docker image

```
docker build -t simplifi .
docker run -d -p 5000:5000 simplifi
```

#### Step 4. Open your browser and go to http://localhost:5000/

Type your query into the search bar. Make sure to include the stock ticker of a public company such as $FB (Facebook) or $XOM (Exxon-Mobil).




## Reference

Yu Chen, Lingfei Wu, Mohammed J. Zaki. **"Bidirectional Attentive Memory Networks for Question Answering over Knowledge Bases."** *In Proc. 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT2019). June 2019.*
