import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import tensorflow 

from tensorflow.keras.models import load_model
model = load_model('Dexter_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    print(sentence_words)
    return sentence_words
#the clean_up_sentence function is up and working

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                print(bag[i])
                if show_details:
                    print ("found in bag: %s" % w)
    print("this assigns 1 for each for input word in the word, ie intents and 0 otherwise")
    print(np.array(bag))
    return(np.array(bag))

#the predict_class is always returning hospital search
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=True)
    print(p)
    res = model.predict(np.array([p]))[0]
    #incorrect probability values.
    #options available, coming from model and predicting values
    

    print("res(this gives the probability): ", end = " ")
    print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    print(enumerate(res))
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    print("user message: " +sentence)
    print(results)
    print(return_list)
    print("\n\n")
    
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

##this code contains the gui
from tkinter import *


def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    def_reply = "Hey, im still under development,\nkindly take it cool with me!"
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatArea.config(state=NORMAL)
        ChatArea.insert(END, "You: " + msg + '\n\n')
        ChatArea.config(foreground="#442265", font=("Verdana", 11))
        
        
        ChatArea.tag_configure('bot_reply_color', foreground='#850f2c')

        res = chatbot_response(msg)
        ChatArea.insert(END, "Dexter: " + res + '\n\n', ('bot_reply_color'))
        ChatArea.config(state=DISABLED)
        ChatArea.yview(END)


# this creates the window and set its properties
window = Tk()
window.title("Dexter | your smart assistant")
window.geometry("400x500")
window.resizable(width=False, height=False)

# the down footer
footer = Label(window,
               text="Dexter© 2020", bd=0, fg="white", bg="black", width=30, height=5
               )
# the chat area
ChatArea = Text(window, bd=0, bg="white", height="8", width="50", font="Arial", )
ChatArea.insert(END, "Dexter: Welcome, I'm your personal assistant.\nHow may i help you?" + '\n\n', ('bot_reply_color'))
ChatArea.tag_configure('bot_reply_color', foreground='#850f2c',font=("Verdana", 11))
ChatArea.config(state=DISABLED)

# Bind scrollbar to chat area
scrollbar = Scrollbar(window, command=ChatArea.yview, cursor="heart")
ChatArea['yscrollcommand'] = scrollbar.set

# Create Button to send message
SendButton = Button(window, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#387ed9", activebackground="#3c9d9b", fg='#ffffff',
                    command=send
                    )

# Create the box to enter message
EntryBox = Text(window, bd=0, bg="white", width="29", height="5", font="Arial")

# EntryBox.bind("<Return>", send)


# Place all components on the screen
scrollbar.place(x=376, y=6, height=392)
ChatArea.place(x=6, y=6, height=392, width=370)
EntryBox.place(x=6, y=400, height=60, width=287)
SendButton.place(x=300, y=400, height=60, width=95)
footer.place(x=0, y=470, height=30, width=400)

# this should be the last item
window.mainloop()
