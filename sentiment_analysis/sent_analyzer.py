from textblob import TextBlob
import nltk
nltk.download('punkt')
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import string


def remove_next_line_chars(input_text):
    input_text = ' '.join([i.strip() for i in input_text.split('\n')])
    return input_text


def reduce_lengthening(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)



# For a test on English: sentence = "Today is a good day. من	ونرتاح	ويدعون"
def remove_non_ascii_prinatble(sentence):
    ascii_chs = set(string.printable)  # speeds things up
    list_of_words = sentence.split()
    list_of_words = [word for word in list_of_words 
            if all(char in ascii_chs for char in word)]
    result = " ".join(list_of_words)
    return result


def stem_sentence(sentence):
    porter = nltk.PorterStemmer()
    token_words=word_tokenize(sentence) 
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    #removing special chars
    stem_sentence =  [word + " " for word in stem_sentence if word.isalnum()]
    return "".join(stem_sentence)


def classify(sentence):
    blob = TextBlob(sentence)
    return blob.sentiment.polarity

def num_to_cat_binning(polarity):
    if(polarity > 0.3):
        return "positive"
    elif(polarity < -0.3):
        return "negative"
    else:
        return "neutral"


def return_labeled_df(dataframe):
    step_1_series = dataframe['comment'].apply(remove_next_line_chars)
    step_2_series = step_1_series.apply(reduce_lengthening)
    
    dataframe['clean_comment'] = step_2_series.apply(remove_non_ascii_prinatble)
    dataframe['stemmed_text'] = dataframe['clean_comment'].apply(stem_sentence)

    dataframe['sentiment_value'] = dataframe['clean_comment'].apply(classify)
    dataframe['Output'] = dataframe['sentiment_value'].apply(num_to_cat_binning)
    return dataframe

# df = pd.read_csv("/home/srimanth/Programs/project_4-2/ytube_clean.csv")
# print(return_labeled_df(df))
