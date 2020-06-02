# recommenderSystem

The vast majority of B2C services are quickly discovering the strategic importance of solid recommendation engines to improve the conversion rates and to establish a stronger fidelity with the customers. The most common strategies are based on the segmentation of users according to their personal features (age range, gender, interests, social interactions, and so on) or to the ratings they gave to specific items. The latter approach normally relies on explicit feedbacks (e.g. a rating from 0 to 10) which summarize the overall experience. Unfortunately, there are drawbacks to both cases.

Personal data is becoming harder to retrieve and the latest regulations (i.e. GDPR) allow the user to interact with a service without the collection of data. Moreover, a reliable personal profile must be built using many attributes that are often hidden and can only be inferred using predictive models. Conversely, implicit feedbacks are easy to collect but they are extremely scarce. Strategies based on the factorization of the user-item matrix are easy to implement (considering the possibility to employ parallelized algorithms), but the discrepancy between the number of ratings and number of products is normally too high to allow an accurate estimation.

Our experience showed that it’s possible to create very accurate user profiles (also for an anonymous user identified only by a random ID) exploiting the implicit feedbacks.


Stack used: Apache Spark, Python3, Flask, conda, apache-airflow, bs4, frozendict, geopy, ipython==5.0, kafka-python, matplotlib, numpy, py4j, pyelasticsearch, pymongo, requests, scipy, selenium, sklearn, tabulate, tldextract, wikipedia, findspark, iso8601, notebook==5.0.0, beautifulsoup4, networkx, jupyter, nltk, gensim, futures, deepwalk, tornado==4.5.3
