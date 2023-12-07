import pandas as pd
import matplotlib as plt
import seaborn as sns
import numpy as np
import re


def create_df_with_datetime(file_name):
    df = pd.read_csv(f'/kaggle/input/ipl2020-tweets/{file_name}.csv')
#     df = pd.read_csv('/kaggle/input/new-york-city-transport-statistics/mta_1706.csv')
    return df


df1 = create_df_with_datetime("IPL2020_Tweets")

# Fill null values in the specific column with the specific string
df1['is_retweet'].fillna(False, inplace=True)
df1['source'].fillna("Twitter for Android", inplace=True)
df1['hashtags'].fillna("['IPL2020']", inplace=True)
df1['user_description'].fillna("description", inplace=True)

# Since user_location is importance variable as naturally, can't impute by a sample data. so dropped it
# Drop rows with null values in the 'user_location' column
df1.dropna(subset=['user_location'], inplace=True)

# Get all the column names as a list
columns = df1.columns.tolist()

# Remove leading and trailing spaces for all columns
df1[columns]=df1[columns].apply(lambda x: x.str.strip() if x.dtype=='object' else x)

# convert date column into string
df1['date'] = df1['date'].astype(str)
df1['day'] = df1['date'].str[-2:]

# assign data types to the columns
df1['user_name'] = df1['user_name'].astype(str)
df1['user_location'] = df1['user_location'].astype(str)
df1['user_description'] = df1['user_description'].astype(str)
df1['user_created'] = df1['user_created'].astype(str)
df1['user_followers'] = df1['user_followers'].astype(int)
df1['user_friends'] = df1['user_friends'].astype(int)
df1['user_favourites'] = df1['user_favourites'].astype(int)
df1['user_verified'] = df1['user_verified'].astype(bool)
df1['text'] = df1['text'].astype(str)
df1['hashtags'] = df1['hashtags'].astype(str)
df1['source'] = df1['source'].astype(str)
df1['is_retweet'] = df1['is_retweet'].astype(bool)
df1['day'] = df1['day'].astype(int)
df1['month'] = df1['month'].astype(int)
df1['year'] = df1['year'].astype(int)

def remove_links(df1):
    link_pattern = re.compile(r'https?://\S+|www\.\S+')

    for column in columns:
        df1[column] = df1[column].apply(lambda text: re.sub(link_pattern, '', str(text)))

    return df1


def remove_special_characters(df1):
    special_character_pattern = re.compile(r"[^\w\s']")

    for column in columns:
        df1[column] = df1[column].apply(lambda text: re.sub(special_character_pattern, ' ', str(text)))

    return df1


def lowercase_all_columns(df1):
    for column in columns:
        df1[column] = df1[column].apply(lambda text: str(text).lower())
    return df1


# Contractions mapping
contractions_mapping = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "I'd": "I would",
    "I'll": "I will",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it's": "it is",
    "let's": "let us",
    "mustn't": "must not",
    "shan't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "we'd": "we would",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "where's": "where is",
    "who's": "who is",
    "who'll": "who will",
    "who're": "who are",
    "who've": "who have",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
}


def expand_contractions(text):
    words = text.split()
    expanded_words = [contractions_mapping[word] if word in contractions_mapping else word for word in words]
    return " ".join(expanded_words)


def expand_all_contractions(df1):
    for column in columns:
        df1[column] = df1[column].apply(expand_contractions)
    return df1


def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def remove_emojis_in_columns(df1):
    for column in columns:
        df1[column] = df1[column].apply(remove_emojis)
    return df1


from googletrans import Translator

columns_to_filter = ['user_location', 'user_description', 'text', 'hashtags']


def translate_to_english(text):
    try:
        translation = Translator.translate(text, src='auto', dest='en')
        return translation.text
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text


def translate_columns_to_english(df1, columns_to_filter):
    translator = Translator()

    for column in columns_to_filter:
        df1[column] = df1[column].apply(translate_to_english)

    return df1



remove_links(df1)
expand_all_contractions(df1)
lowercase_all_columns(df1)
remove_emojis_in_columns(df1)
# translate_columns_to_english(df1, columns_to_filter)


# dropped the date column since extracted day, month, year seperate features & dropped user_created since not usable
df1.drop('user_created', axis=1, inplace=True)
df1.drop('date', axis=1, inplace=True)
# Reorder the columns to place the "day" column after the "is_retweet" column
df1 = df1.reindex(columns=['user_name', 'user_location', 'user_description', 'user_followers', 'user_friends', 'user_favourites', 'user_verified', 'text', 'hashtags', 'source', 'is_retweet', 'day', 'month', 'year'])

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import nltk
nltk.download('punkt')
nltk.download('stopwords')


# List of all countries to check against
all_countries = [
    "afghanistan", "albania", "algeria", "andorra", "angola", "antigua and barbuda",
    "argentina", "armenia", "australia", "austria", "azerbaijan", "bahamas", "bahrain",
    "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", "bhutan", "bolivia",
    "bosnia and herzegovina", "botswana", "brazil", "brunei", "bulgaria", "burkina faso",
    "burundi", "cabo verde", "cambodia", "cameroon", "canada", "central african republic",
    "chad", "chile", "china", "colombia", "comoros", "congo", "costa Rica", "cote d'ivoire",
    "croatia", "cuba", "cyprus", "czech Republic", "Democratic Republic of the Congo",
    "denmark", "djibouti", "dominica", "dominican republic", "east timor (timor-leste)",
    "ecuador", "egypt", "el salvador", "equatorial guinea", "eritrea", "estonia", "eswatini",
    "ethiopia", "fiji", "finland", "france", "gabon", "gambia", "georgia", "germany", "ghana",
    "greece", "grenada", "guatemala", "guinea", "guinea-bissau", "guyana", "haiti",
    "honduras", "hungary", "iceland", "india", "indonesia", "iran", "iraq", "ireland", "israel",
    "italy", "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kiribati", "korea, north",
    "korea, south", "kosovo", "kuwait", "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho",
    "liberia", "libya", "liechtenstein", "lithuania", "luxembourg", "madagascar", "malawi",
    "malaysia", "maldives", "mali", "malta", "marshall islands", "mauritania", "mauritius",
    "mexico", "micronesia", "moldova", "monaco", "mongolia", "montenegro", "morocco",
    "mozambique", "myanmar (burma)", "namibia", "nauru", "nepal", "netherlands", "new zealand",
    "nicaragua", "niger", "nigeria", "north macedonia", "norway", "oman", "pakistan", "palau",
    "panama", "papua new guinea", "paraguay", "peru", "philippines", "poland", "portugal",
    "qatar", "romania", "russia", "rwanda", "saint kitts and nevis", "saint lucia",
    "saint vincent and the grenadines", "samoa", "san marino", "sao tome and principe",
    "saudi arabia", "senegal", "serbia", "seychelles", "sierra leone", "singapore", "slovakia",
    "slovenia", "solomon islands", "somalia", "south africa", "south sudan", "spain", "sri lanka",
    "sudan", "suriname", "sweden", "switzerland", "syria", "taiwan", "tajikistan", "tanzania",
    "thailand", "togo", "tonga", "trinidad and tobago", "tunisia", "turkey", "turkmenistan",
    "tuvalu", "uganda", "ukraine", "united arab emirates", "united kingdom", "united states",
    "uruguay", "uzbekistan", "vanuatu", "vatican City", "venezuela", "vietnam", "yemen", "zambia",
    "zimbabwe",
]

# Create a set for faster lookups
country_set = set(all_countries)

def extract_country(location):
    words = word_tokenize(location.lower())
    words = [word for word in words if word not in stopwords.words('english') and word in country_set]
    return ', '.join(words) if words else None

df1['country'] = df1['user_location'].apply(extract_country)

# Count rows without a country
no_country_count = df1['country'].isnull().sum()

print("Number of rows without a country:", no_country_count)


from geonamescache import GeonamesCache
from geonamescache.mappers import country

# Initialize the GeonamesCache
gc = GeonamesCache()

# Create a mapper for country codes
country_mapper = country(from_key='iso', to_key='name')

# Get the cities in India
cities_in_india = [city for city in gc.get_cities().values() if country_mapper(city['countrycode']) == 'India']

# Extract city names from the list
city_names_in_india = [city['name'] for city in cities_in_india]

# Print the list of cities in India
city_names_in_india





from collections import Counter

# Convert the "country" column to a list of strings
country_list = df1['country'].dropna().tolist()

# Combine country strings into a single string
all_countries = ' '.join(country_list)

# Split the combined string into words and count occurrences
word_counts = Counter(all_countries.split())

# Print unique words and their occurrences
print("Unique words and their occurrences in the 'country' column:")
for word, count in word_counts.items():
    print(f"{word}: {count}")

import pandas as pd
from geotext import GeoText
from geopy.geocoders import Nominatim
from tqdm import tqdm

df2 = df2[:50]

# Initialize geocoder
geolocator = Nominatim(user_agent="my_geocoder")


def extract_city_country(location):
    try:
        # Use GeoText to identify countries
        places = GeoText(location)
        countries = places.countries

        if countries:
            country = countries[0]

            # Remove the identified country name
            location_without_country = location.replace(country, '').strip()

            # Use geocoder to identify the city within the country
            location_data = geolocator.geocode(location_without_country, exactly_one=True, country_codes=[country])
            if location_data:
                city = location_data.raw.get('address', {}).get('city')
                return city, country
    except Exception as e:
        print(f"Error processing {location}: {e}")
    return None, None


# Use tqdm to add a progress bar
tqdm.pandas()

# Apply the extract_city_country function to the user_location column
df2[['city', 'countri']] = df2['user_location'].progress_apply(extract_city_country)

print("DataFrame with extracted city and country:")
df2



import pandas as pd
from geotext import GeoText
from geopy.geocoders import Nominatim
from tqdm import tqdm

df2 = df1
df2 = df2[:100]
# Initialize geocoder
geolocator = Nominatim(user_agent="my_geocoder")

def extract_city(location):
    try:
        location_data = geolocator.geocode(location, exactly_one=True)
        if location_data:
            return location_data.raw.get('address', {}).get('city')
    except Exception as e:
        print(f"Error geocoding {location}: {e}")
    return None

# Use tqdm to add a progress bar
tqdm.pandas()

# Apply the extract_city function to the user_location column
df2['city'] = df2['user_location'].progress_apply(extract_city)

print("DataFrame with extracted city names:")
df2



# ############################################################





