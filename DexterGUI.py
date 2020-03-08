from tkinter import *


def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    def_reply = "Hey, im still under development, kindly take it cool with me!"
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatArea.config(state=NORMAL)
        ChatArea.insert(END, "You: " + msg + '\n\n')
        ChatArea.config(foreground="#442265", font=("Verdana", 11))

        ChatArea.tag_configure('bot_reply_color', foreground='#850f2c')

        # res = chatbot_response(msg)
        ChatArea.insert(END, "Dexter: " + def_reply + '\n\n', ('bot_reply_color'))
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
