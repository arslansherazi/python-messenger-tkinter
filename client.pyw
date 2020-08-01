from tkinter import *
from _thread import *
import socket
import time


def clear():
    text.delete(0, END)
    text1.delete(0, END)


def new_window():
    p = port.get()
    n = name.get()
    win.configure(background="white")
    win.geometry("500x500")
    win.title(n)
    win.resizable(width=False, height=False)

    upper_m = Frame(win, bg="lightblue")
    upper_m.place(x=0, y=0, width=150, height=30)

    left = Frame(win, bg="lightblue")
    left.place(x=0, y=31, width=150, height=470)

    message_win = Text(left, bg="lightblue")
    message_win.place(x=0, y=0, width=150, height=500)
    message_win.configure(state="disabled")

    scroll_bar = Scrollbar(left)
    scroll_bar.pack(side=RIGHT, fill=Y)
    message_win['yscrollcommand'] = scroll_bar.set
    scroll_bar.config(command=message_win.yview)

    upper = Frame(win, bg="white")
    upper.place(x=150, y=0, width=350, height=60)

    center = Frame(win, bg="white")
    center.place(x=150, y=60, width=350, height=390)

    second_message_win = Text(center, bg="white")
    second_message_win.place(x=0, y=0, width=350, height=390)
    second_message_win.configure(state="disabled")

    scrollbar = Scrollbar(center)
    scrollbar.pack(side=RIGHT, fill=Y)
    second_message_win['yscrollcommand'] = scrollbar.set
    scrollbar.config(command=second_message_win.yview)

    connect_client(p, n, win, second_message_win, message_win)

    win.mainloop()


def connect_client(port, name, win, message_win, second_message_win):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = port
    client.connect((host, port))
    client.send(bytes(name, 'utf-8'))

    def threaded_receive(client, inc, win, message_win):
        while True:
            tok = client.recv(1024)
            print(tok)
            if tok == bytes("name", 'utf-8'):
                inc = inc + 30
            elif tok == bytes("message", 'utf-8'):
                border_line = Label(
                    win, text="____________________________", font=('Berlin Sans FB', 20), fg="lightblue", bg="white"
                )
                border_line.place(x=150, y=25)

                name = client.recv(1024)
                msg = client.recv(1024)

                label = Label(win, text="Received Message From", bg="white")
                label.place(x=150, y=20)
                label = Label(win, text=name, font=("Berlin Sans FB", 10, 'bold'), bg="white", fg="#FFBE4A")
                label.place(x=280, y=20)

                message_win.configure(state="normal")
                message_win.insert(END, name)
                message_win.insert(END, ':')

                message_win.insert(END, '\n')
                message_win.insert(END, '    ')
                message_win.insert(END, msg)
                message_win.insert(END, '\n')
                message_win.insert(END, '\n')

                message_win.configure(state="disabled")

                bottom = Frame(win, bg="#FFBE4A")
                bottom.place(x=150, y=450, width=300, height=50)

                message = Text(bottom, bg="#FFBE4A")
                message.place(x=5, y=5, width=290, height=40)
                send = Button(
                    win, text="Send", bg="lightblue", fg="white", width=7, font=("Calibri", 10, 'bold'), height=3,
                    command=lambda: communication_handling(message, win, client, name, message_win)
                )
                send.place(x=450, y=450)

    i = 20
    start_new_thread(threaded_receive, (client, i, win, message_win, second_message_win))


def communication_handling(message, client, user, message_win):
    msg = message.get("0.0", "end-1c")
    message.delete("0.0", "end-1c")
    message_win.configure(state="normal")
    message_win.insert(END, "You to ")
    message_win.insert(END, user)
    message_win.insert(END, ':')
    message_win.insert(END, '\n')
    message_win.insert(END, '    ')
    message_win.insert(END, msg)
    message_win.insert(END, '\n')
    message_win.insert(END, '\n')
    message_win.configure(state="disabled")
    send_message(msg, user, client)


def send_message(msg, user, client):
    token = "message"
    client.send(bytes(token, 'utf-8'))
    time.sleep(1)
    client.send(user)
    time.sleep(1)
    client.send(bytes(msg, 'utf-8'))
    time.sleep(1)


class ButtonHandler(object):
    def __init__(self, user, win, online_user, i, client, message_win):
        online_user.append(Button(
            win, text=user, bg="lightblue", fg="white", font=("Calibri", 10), width=17,
            command=lambda: self.send_receive(user, client, win, message_win)).place(x=2, y=i)
        )

    def send_receive(self, user, client, win, message_win):
        label = Label(win, text="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", bg="white",
                      fg="white")
        label.place(x=150, y=0)

        border_line = Label(win, text="____________________________", font=('Berlin Sans FB', 20), fg="lightblue",
                            bg="white")
        border_line.place(x=150, y=25)

        label = Label(win, text="You are Connect with", bg="white")
        label.place(x=150, y=0)
        label = Label(win, text=user, font=("Berlin Sans FB", 10, 'bold'), bg="white", fg="#FFBE4A")
        label.place(x=270, y=0)
        bottom = Frame(win, bg="#FFBE4A")
        bottom.place(x=150, y=450, width=300, height=50)
        message = Text(bottom, bg="#FFBE4A")
        message.place(x=5, y=5, width=290, height=40)
        send = Button(win, text="Send", bg="lightblue", fg="white", width=7, font=("Calibri", 10, 'bold'), height=3,
                      command=lambda: communication_handling(message, win, client, user, message_win))
        send.place(x=450, y=450)


if __name__ == '__main__':
    win = Tk()
    win.configure(background="#00AFF0")
    win.title("iMessenger")
    win.geometry("500x500")
    win.wm_iconbitmap('icon.ico')
    win.resizable(width=False, height=False)

    l1 = Label(text="Welcome to", bg="#00AFF0", fg="white", font=('Calibri', 20))
    l1.pack()
    l2 = Label(text="iMessenger", bg="#00AFF0", fg="white", font=('Calibri', 40))
    l2.pack()

    port = IntVar()
    name = StringVar()

    l3 = Label(text="Enter Your Name", bg="#00AFF0", fg="white", font=('Calibri', 15))
    l3.place(x=80, y=250)
    text = Entry(win, textvariable=name)
    text.place(x=260, y=255)

    l4 = Label(text="Port No", bg="#00AFF0", fg="white", font=('Calibri', 15))
    l4.place(x=80, y=200)
    text1 = Entry(win, textvariable=port)
    text1.place(x=260, y=202)

    clear()

    enter = Button(win, text="Enter", bg="lightblue", fg="black", font=('Calibri', 20), width=10, command=new_window)
    enter.place(x=90, y=350)

    reset = Button(win, text="Reset", bg="lightblue", fg="black", font=('Calibri', 20), width=10, command=clear)
    reset.place(x=250, y=350)

    win.mainloop()
