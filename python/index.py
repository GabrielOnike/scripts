import re
import csv
import wikipedia
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# %matplotlib inline
# above we import wikipedia to get wikipedia library
# we import re to access the ReGex library
# we import csv to handle our csv file manipulations
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# Start with loading all necessary libraries by installing with:pip3 install pandas, pip3 install numpy etc. 
# RE:If you’re working in the Jupyter environment, uncomment the %matplotlib inline above for Jupyter magic to display the histogram inline.



# Specify the title of the Wikipedia page
wiki = wikipedia.page('SpaceX')

# Extract the plain text content of the page, excluding images, tables, and other data.
text = wiki.content

# Replace '==' with '' (an empty string)
text = text.replace('==', '')

# Replace '\n' (a new line) with '' & end the string at $1000.
text = text.replace('\n', '')[:-12]
#print(text)

# define punctuation
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

#below converts a list of text strings and stores it to the txt file format stated within
with open('wiki-spaceX.txt', 'a') as f:
    f.writelines(text)


#empty fileText array to be filled later by function below
fileText=[]

#below we open the saved txt file and convert it to a string
with open('wiki-spaceX.txt') as f:
    fileText = f.read()  
    #store filetext as a string to the textString variable below 
    textString = str(fileText)

#we remove punctuations from the string by comparing it to the punctuation array above and saving it to no_punct
no_punct = ""
for char in fileText:
   if char not in punctuations:
       no_punct = no_punct + char

#no_num then removes all numbers from the no_punct list
no_num = re.sub(r'\d+', '', no_punct)

#now_lower then changes all the values in no_num to small letters
now_lower = no_num.lower()


# the function below takes the text in now_lower, splits the words to single strings, then counts its frequency
def word_count(now_lower):
    counts = dict()
    words = now_lower.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts    

#dict_count variable stores the results of word_count 
dict_count = word_count(now_lower)

#below converts dict_count into a dictionary
rdict_count= dict(dict_count)

#here we create a wordCLoud using our pandas import
wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(rdict_count)

#we use matplot to describe the dimensions and actions of the wordcloud
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)

# TASK - we store the wordcloud as a png in the root folder
wordcloud.to_file("wordcloud_spaceX.png")



#below creates csv file, opens it,creates headers and then writes the dictionary under each header as a csv file
with open('wordcount.csv', 'w', newline='') as csvfile:
    header_key = ['Word', 'Frequency']
    write_dict = csv.DictWriter(csvfile, fieldnames=header_key)

    write_dict.writeheader()
    for item in rdict_count:
        write_dict.writerow({'Word': item, 'Frequency': rdict_count[item]})



# Next steps describe the data in our csv after reading it
# create data frame 
data = pd.read_csv("wordcount.csv") 
    
# removing null values to avoid errors 
data.dropna(inplace = True) 
  
# calling describe method
desc = data["Word"].describe()
descTwo = data["Frequency"].describe()
  
# display the description of desc(word) and descTwo(Frequency) of the Word and Frequency in your console
# print(desc,descTwo)
# display description of entire csv
print(data.describe())

# Next,using matplot we show the histogram of Word from our csv file
plt.hist(data)
plt.show()
