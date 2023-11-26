import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from gensim.models import CoherenceModel

# Load your dataset
# Assuming 'tweets.csv' is the name of your dataset
df = pd.read_csv('df1_cleaned_final.csv')
df = df[:1000]
# Preprocess the text data
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess_text(text):
    tokens = word_tokenize(str(text).lower())
    tokens = [ps.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
    return tokens

df['processed_text'] = df['text'].apply(preprocess_text)

# Create a dictionary and a corpus
dictionary = corpora.Dictionary(df['processed_text'])
corpus = [dictionary.doc2bow(tokens) for tokens in df['processed_text']]

# Build the LDA model
num_topics = 5  # You can adjust this based on the number of topics you want to identify
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

# Print the topics and the words associated with each topic
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(topic)

# Compute coherence score to evaluate the model
coherence_model_lda = CoherenceModel(model=lda_model, texts=df['processed_text'], dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score:', coherence_lda)