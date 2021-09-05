import json
import pickle
import string
from tokenize import tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords

# nltk.download('vader_lexicon')
# nltk.download('state_union')


def get_text_processing(txt):
    stop_word = stopwords.words('english')
    no_punctuation = [char for char in txt if char not in string.punctuation]
    no_punctuation = ''.join(no_punctuation)
    return ' '.join([word for word in no_punctuation.split() if word.lower() not in stop_word])


def analyze_text(text):

    words = nltk.word_tokenize(get_text_processing(text))
    if words:
        f = nltk.Text(words)
        fd = f.vocab()
        fd.tabulate(5)

        sia = SentimentIntensityAnalyzer()
        word_dict = {'common': dict(fd.most_common(5)), 'sent': sia.polarity_scores(text)}
        encode = json.dumps(word_dict)
        return encode
    return 'Empty'


if __name__ == '__main__':
    print("From inside")
