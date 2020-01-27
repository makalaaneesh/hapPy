- ## Abstract
    - Every day, thousands suffering from mental illnesses like anxiety and depression post on social media. For example, on reddit, there is a subreddit for depression (https://www.reddit.com/r/depression/) where people can vent and express their feelings. Searching for #depression on twitter gives many tweet results by depressed people. This project aims to build a twitter bot (or a bot for any text-based social media platform) that does two tasks:
        - Identify if the tweet has signals of mental illnesses.
        - Reply to the tweet with an inspiring, relevant quote (from a corpus of quotes) that can help the person get a wider and better perspective, thus, helping them get out of their mental rut. 
    - Check it out at https://twitter.com/hapybot/with_replies
- ## How it works
    - ### Identifying if the tweet has signals of mental illnesses
        - For task 1, to identify whether the tweet's text has signals of mental illnesses or not, a machine learning binary classification model is used. Till now, the following models have been tried out:
            - Naive Bayes with TFIDF text embedding
            - SVM with TFIDF text embedding
        - Future Work
            - Explore other classification models
            - Explore deep learning based text embeddings like word2vec, BERT, etc
    - ### Reply to the tweet with an inspiring quote.
        - For now, there is a corpus of generic uplifting quotes from which a random quote is chosen.
        - Future Work
            - Define relevance and build an algorithm to pick a relevant quote from the corpus.
- ## Engineering
    - ### Data flow
        
        - tweepy StreamListener is used to process a stream of incoming tweets
        - The raw tweets are ingested into a kafka topic
        - The "preprocess" consumer consumes the raw tweets, preprocesses them and puts them on another kafka topic.
        - The preprocessed tweets are consumed by the "predict" consumer which classifies the tweet into either having signs of mental illness (1) or not (0). The positive tweets are put on another kafka topic. The negative tweets are discarded
        - The positive tweets are finally loaded into MongoDB.
        - Periodically (orchestrated by Airflow), the "send replies" process wakes up, reads "n" positive tweets from MongoDB, finds a relevant quote and then replies to the original tweet using the tweepy Twitter API.
    - ### Design/Tools/Framework choices
        - **Why Kafka?**
            - The rate of incoming tweets will be higher that the rate at which the tweets are processed (preprocess, classify, etc). Therefore, a data pipeline is used.
            - Low coupling between different processes of "preprocess", "predict", etc In future, if there is a need to test multiple models, it would be as easy as launching a new "predict" consumer.
            - Scalability and Reliability
                - Because of the low coupling, the consumers(processors) and the producers(from social media) can be scaled individually. 
                - If one kafka process goes down, the others don't, and parts of the the system will still run during the repair time.
        - **Why store to DB?**
            - Ideally, the data pipeline's last process could have been responsible of sending replies to the tweets, but the bot would get blocked by Twitter by posting at the (nearly) same rate as it is consuming.
            - Why NOSQL (MongoDB)?
                - The data model does not involve relations between different entities.
                - Consistency  and isolation between the classifier and the twitter bot is not a major concern.
                - NoSQL databases are easier to scale.
        - **Why Airflow?**
            - To orchestrate scheduling the workflow for various tasks:
                - Stream new tweets every 't' hours and store to DB
                - Extract 'n' tweets and send replies every 't' minutes.
                - perform analytics, such as wordcount, to build a wordcloud.
