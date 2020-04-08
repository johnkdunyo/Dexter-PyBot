#lets import our packages, always make sure your packages are up todate
import tensorflow as tf
import nltk
import pickle as pk
import os

print("Always make sure you're using latest versions for best result\n")
print("Tensorflow version : " + tf.__version__)
print("NLTK verrsion : " + nltk.__version__)
print("Keras version : " + tf.keras.__version__)
print("Pickle version : "+ pk.format_version)
print("\n\n")

import json
import numpy as np
import random
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


words = []
classes = []
documents= []
ignore_words = ['?', '!', '.']
custom_file = open('intents.json').read()
intents = json.loads(custom_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        #we tokenize each word
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        
        #add documents in the corpus
        documents.append((w, intent['tag']))
        
        #add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            

# lemmatize, lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
# sort classes
classes = sorted(list(set(classes)))
# documents = combination between patterns and intents
print (len(documents), "documents")
print("\n\n")
# classes = intents
print (len(classes), "classes", classes)
print("\n\n")
# words = all words, vocabulary
print (len(words), "unique lemmatized words", words)
print("\n\n")
pk.dump(words,open('words.pkl','wb'))
pk.dump(classes,open('classes.pkl','wb'))


# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(classes)
# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
for w in words:
    bag.append(1) if w in pattern_words else bag.append(0)
    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])
# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])

print("\n\n")
#print(training)
print("............................Training data created............................")

# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))


# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model 
hist = model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=5, verbose=1)

print("Saving model\n")

model.save('Dexter_model.h5', hist)
print("\nModel created and saved succesfully as Dexter_model.h5 at : \n", os.path.dirname(os.path.abspath(__file__)))

print("\n\n")

print("Done\nRun the DexterGui.py to continue")