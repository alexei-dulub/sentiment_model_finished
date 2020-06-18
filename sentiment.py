import random
from nltk import classify, pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.classify.naivebayes import NaiveBayesClassifier

class Analyzer:
    def __init__(self):
        """
        Gather data
        """
        positive = twitter_samples.strings('positive_tweets.json')
        negative = twitter_samples.strings('negative_tweets.json')
        self.stop_words = list(set(stopwords.words('english')))

        positive_tokens = twitter_samples.tokenized('positive_tweets.json')
        negative_tokens = twitter_samples.tokenized('negative_tweets.json')

        """
        Clean the data
        """
        positive_clean = []
        negative_clean = []

        for token in positive_tokens:
            positive_clean.append(self.clean(token))

        for token in negative_tokens:
            negative_clean.append(self.clean(token))

        positive_model_tokens = self.final_token_generator(positive_clean)
        negative_model_tokens = self.final_token_generator(negative_clean)

        """
        Use generator to make datasets
        """
        positive_dataset = [(token, "Positive") for token in positive_model_tokens]

        negative_dataset = [(token, "Negative") for token in negative_model_tokens]

        dataset = positive_dataset + negative_dataset

        """
        Shake it all about
        """
        random.shuffle(dataset)
        random.shuffle(dataset)
        random.shuffle(dataset)

        """
        Split them up
        """
        training = dataset[:7000]
        testing = dataset[7000:]

        """
        Train the classifier
        """
        self.classifier = NaiveBayesClassifier.train(training)

        """
        Uncomment these for more data fun :D
        """
        # print("Accuracy:", classify.accuracy(classifier, testing))
        # print(classifier.show_most_informative_features(10))


    """
    Take in an input and run it through the classifier to get its sentiment rating (Positive || Negative)
    """
    def analyze(self, input):
        custom_tokens = self.clean(word_tokenize(input))
        return self.classifier.classify(dict([token, True] for token in custom_tokens))

    """
    Used to clean up the data through various methods
    """
    def clean(self, tokens):
        tokens = [x for x in tokens if not x in self.stop_words]
        l = WordNetLemmatizer()
        lemmatized = []
        for word, tag in pos_tag(tokens):
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            lemmatized.append(l.lemmatize(word, pos))
        return lemmatized

    """
    Generator for making the data into the correct shape
    """
    def final_token_generator(self, tokens):
        for tokens in tokens:
            yield dict([token, True] for token in tokens)