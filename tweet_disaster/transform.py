import functools
import string
import re
from nltk.corpus import words, stopwords
from nltk.stem import WordNetLemmatizer


def filter_printable(text):
    return ''.join(list(filter(lambda ch: ch in string.printable, text)))


def remove_links(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)


def remove_punctuations(text):
    return ''.join(list(filter(lambda ch: ch not in string.punctuation, text)))


def to_lowercase(text):
    return text.lower()


english_words = set(words.words())


def remove_nonwords(text):
    return ' '.join(list(filter(lambda word: word in english_words, text.split(' '))))


def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    ws = text.split(' ')
    for tag in ['a', 'r', 'n', 'v']:
        ws = list(map(lambda w: lemmatizer.lemmatize(w, tag), ws))
    return ' '.join(ws)


english_stopwords = set(stopwords.words('english'))


def remove_stop_words(text):
    return ' '.join(list(filter(lambda w: w not in english_stopwords, text.split(' '))))


city_to_country = {
    'United States': 'USA',
    'New York': 'USA',
    "London": 'UK',
    "Los Angeles, CA": 'USA',
    "Washington, D.C.": 'USA',
    "California": 'USA',
    "Chicago, IL": 'USA',
    "Chicago": 'USA',
    "New York, NY": 'USA',
    "California, USA": 'USA',
    "FLorida": 'USA',
    "Nigeria": 'Africa',
    "Kenya": 'Africa',
    "Everywhere": 'Worldwide',
    "San Francisco": 'USA',
    "Florida": 'USA',
    "United Kingdom": 'UK',
    "Los Angeles": 'USA',
    "Toronto": 'Canada',
    "San Francisco, CA": 'USA',
    "NYC": 'USA',
    "Seattle": 'USA',
    "Earth": 'Worldwide',
    "Ireland": 'UK',
    "London, England": 'UK',
    "New York City": 'USA',
    "Texas": 'USA',
    "London, UK": 'UK',
    "Atlanta, GA": 'USA',
    "Mumbai": "India"}


def drop_id_columns(df):
    return df.drop(columns='id', axis=1)


def process_text(df):
    for f in [filter_printable, remove_links, remove_punctuations, to_lowercase,
              remove_nonwords, lemmatize, remove_stop_words]:
        df['text'] = df['text'].apply(f)
    return df


def process_keywords(df):
    df['keyword'] = df['keyword'].fillna('none')
    df['keyword'] = df['keyword'].astype('str').apply(lambda x: x.replace('%20', '_'))
    return df


def process_location(df):
    df['location'] = df['location'].replace(city_to_country)
    df['location'] = df['location'].fillna('Worldwide')
    return df


def rename_columns(df):
    return df.rename(columns={
        'keyword': 'KEYWORD',
        'location': 'LOCATION',
        'text': 'TEXT',
        'target': 'TARGET'
    })


def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


transform = compose(
    rename_columns,
    process_keywords,
    process_location,
    process_text,
    drop_id_columns
)
