from __future__ import annotations
from tkinter import *
from tkinter import messagebox
import os
import pandas as pd
import time
from collections.abc import Iterable, Iterator
from typing import Any, List


class User:
    def __init__(self):
        window = User.create_window(780, 400)
        Label(window, text="Добро пожаловать в программу изучения языков \n LanguageLearn!",
              font=("Arial Bold", 30)).grid(column=0, row=0, padx=10, pady=10)
        Button(window, text="Зарегистрироваться", fg="black",
               command=lambda: User.clicked_sign_up(window)).grid(column=0, row=1, padx=10, pady=10)
        Button(window, text="Уже зарегистрирован!", fg="black",
               command=lambda: User.clicked_sign_in(window)).grid(column=0, row=2, padx=10, pady=10)
        window.mainloop()

    def create_window(W, H):
        window = Tk()
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        w = w // 2
        h = h // 2
        w = w - W // 2
        h = h - H // 2
        window.title("EnglishLearn")
        window.geometry('{}x{}+{}+{}'.format(W, H, w, h))
        window.resizable(False, False)
        return window

    def clicked_sign_up(window):
        window.destroy()
        window = User.create_window(780, 400)
        Label(window, text="Придумайте логин и пароль", font=("Arial Bold", 30)).place(x=10, y=10)
        Label(window, text="Логин: ", font=("Arial Bold", 30)).place(x=30, y=50)
        login = StringVar()
        password = StringVar()
        Entry(window, width=20, textvariable=login).place(x=160, y=60)
        Label(window, text="Пароль: ", font=("Arial Bold", 30)).place(x=30, y=100)
        Entry(window, width=20, textvariable=password).place(x=160, y=110)
        Button(window, text='Зарегистрироваться', fg="black", background="#555", padx=10, pady=10,
               command=lambda: User.sign_up(window, login, password)).place(x=200, y=180)
        window.mainloop()

    def clicked_sign_in(window):
        window.destroy()
        window = User.create_window(780, 400)
        Label(window, text="Введите логин и пароль", font=("Arial Bold", 30)).place(x=10, y=10)
        Label(window, text="Логин: ", font=("Arial Bold", 30)).place(x=30, y=50)
        login = StringVar()
        password = StringVar()
        Entry(window, width=20, textvariable=login).place(x=160, y=60)
        Label(window, text="Пароль: ", font=("Arial Bold", 30)).place(x=30, y=100)
        Entry(window, width=20, textvariable=password).place(x=160, y=110)
        Button(window, text='Войти', fg="black", background="#555", padx=10, pady=10,
               command=lambda: User.sign_in(window, login, password)).place(x=200, y=180)
        window.mainloop()

    def sign_up(window, login, password):
        path = os.getcwd()
        path += "/users.csv"
        if len(login.get()) <= 3:
            messagebox.showinfo("Ошибка", "Логин слишком короткий!")
            return
        if len(password.get()) <= 3:
            messagebox.showinfo("Ошибка", "Пароль слишком короткий!")
            return
        if os.path.exists(path):
            users_old = pd.read_csv('users.csv')
            for i in users_old['login']:
                if i == login.get():
                    messagebox.showinfo("Ошибка", "Логин: " + login.get() + " уже занят!")
                    return
            users_new = pd.DataFrame(data=[[login.get(), password.get()]], columns=['login', 'password'])
            users_new = pd.concat([users_old, users_new])
            users_new.to_csv("users.csv", index=False)
            path = os.getcwd()
            path += "/Users/" + login.get()
        else:
            file = open("users.csv", "w")
            users_new = pd.DataFrame(data=[[login.get(), password.get()]], columns=['login', 'password'])
            users_new.to_csv("users.csv", index=False)
            file.close()
            path = os.getcwd()
            path += "/Users"
            try:
                os.mkdir(path)
            except OSError:
                print()
            path += "/" + login.get()
        try:
            os.mkdir(path)
        except OSError:
            print()
        window.destroy()
        words = pd.read_csv('Content/Внешность.csv')
        words.to_csv('Users/' + login.get() + "/Внешность.csv")
        words = pd.read_csv('Content/Все слова.csv')
        words.to_csv('Users/' + login.get() + "/Все слова.csv")
        words = pd.read_csv('Content/Погода.csv')
        f = open("Users/" + login.get() + "/Погода.csv", "w")
        words.to_csv('Users/' + login.get() + "/Погода.csv")
        User.main_page(login)

    def sign_in(window, login, password):
        path = os.getcwd()
        path += "/users.csv"
        if len(login.get()) <= 3:
            messagebox.showinfo("Ошибка", "Логин слишком короткий!12")
            return
        if len(password.get()) <= 3:
            messagebox.showinfo("Ошибка", "Пароль слишком короткий!")
            return
        if os.path.exists(path):
            users_old = pd.read_csv('users.csv')
            for i in range(len(users_old['login'])):
                if users_old['login'][i] == login.get() and users_old['password'][i] == password.get():
                    window.destroy()
                    User.main_page(login)
                    return
            messagebox.showinfo("Ошибка", "Вы ввели неверный логин или пароль!")
        else:
            messagebox.showinfo("Ошибка", "Вы еще не зарегистрировались!")

    def main_page(login):
        window = User.create_window(1200, 700)
        Label(window, text="Личный кабинет",
              font=("Arial Bold", 40)).place(x=450, y=10)
        Label(window, text="Ваши коллекции: ", font=("Arial Bold", 35)).place(x=50, y=80)
        btn = []
        btn.append(Button(window, text="Погода", font=("Arial Bold", 30), width=12, height=3,
                     command=lambda i="Погода": Proxy.training(login, i)))
        btn.append(Button(window, text="Внешность", font=("Arial Bold", 30), width=12, height=3,
                     command=lambda i="Внешность": Proxy.training(login, i)))
        X = 50
        Y = 150
        for i in btn:
            if X < 1200:
                i.place(x=X, y=Y)
                X += 230
            else:
                X = 50
                Y += 150
                i.place(x=X, y=Y)


class Proxy:
    def __init__(self, user: User) -> None:
        self.user = user

    def waiting(self) -> None:
        messagebox.showinfo("Внимание", "Идет подготовка тренировки!")
        time.sleep(1)

    def training(login, name) -> None:
        class Inc:
            def __init__(self, start_state):
                self.state = start_state

            def __call__(self):
                self.state += 1
        k = Inc(0)

        def valid(k, iter, lbl):
            if input.get() == words['translate'][k.state]:
                messagebox.showinfo("Внимание", "Правильно!")
                try:
                    l = next(iter)
                    lbl.config(text=l[0])
                    k()
                except StopIteration:
                    messagebox.showinfo("Внимание", "Тренировка окончена!")
                    window.destroy()

            else:
                messagebox.showinfo("Внимание", "Вы ошиблись!")
        Proxy.waiting(name)
        name += ".csv"
        words = pd.read_csv("Users/" + login.get() + "/" + name)
        window = User.create_window(1200, 700)
        collection = WordsCollection()
        for i in range(len(words['word'])):
            collection.add_item((words['word'][i], words['translate'][i]))
        iter = collection.__iter__()
        l = next(iter)
        lbl = Label(window, text=l[0], font=("Arial Bold", 50))
        lbl.place(x=530, y=100)
        input = Entry(window, width=40, font=("Arial Bold", 30))
        input.place(x=230, y=260)
        Button(window, text='Ввести', fg="black", background="#555", padx=20, pady=20,
               command=lambda: valid( k, iter, lbl)).place(x=500, y=330)
        window.mainloop()


class MyIterator(Iterator):

    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: WordsCollection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):

        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class WordsCollection(Iterable):

    def __init__(self, collection: List[Any] = []) -> None:
        self._collection = collection

    def __iter__(self) -> MyIterator:

        return MyIterator(self._collection)

    def get_reverse_iterator(self) -> MyIterator:
        return MyIterator(self._collection, True)

    def add_item(self, item: Any):
        self._collection.append(item)
