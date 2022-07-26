import pymongo
import certifi
from urllib.request import urlopen
import urllib.request
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextFieldRound, MDTextField
from kivymd.uix.button import MDRectangleFlatButton, MDRectangleFlatIconButton, MDIconButton, MDFillRoundFlatButton
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem, OneLineAvatarIconListItem
from kivy.uix.scrollview import ScrollView
from functools import partial
from kivy.utils import platform
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivymd.uix.label import MDLabel
import time
from kivymd.uix.dialog import MDDialog
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
from kivymd.theming import ThemeManager
from kivy.metrics import dp
import ssl
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
import os
import hashlib

os.environ['SSL_CERT_FILE'] = certifi.where()
from kivy.uix.textinput import TextInput
import re

global value
value = 0


class PredictionApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()

        self.WelcomePage = WelcomePage()
        screen = Screen(name='WelcomeP')
        self.theme_cls.theme_style = "Dark"
        screen.add_widget(self.WelcomePage)
        self.screen_manager.add_widget(screen)


        self.LoginPage = LoginPage()
        screen = Screen(name='LoginP')
        self.theme_cls.theme_style = "Dark"
        screen.add_widget(self.LoginPage)
        self.screen_manager.add_widget(screen)

        self.RegisterPage = RegisterPage()
        screen = Screen(name='RegisterP')
        self.theme_cls.theme_style = "Dark"
        screen.add_widget(self.RegisterPage)
        self.screen_manager.add_widget(screen)

        return self.screen_manager




class WelcomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == "android":

            loginbutton = MDFillRoundFlatButton(text="Login", on_press=self.loginbutton)
            loginbutton.size_hint_x = 0.3
            loginbutton.size_hint_y = 0.1
            loginbutton.pos_hint = {'x': .35, 'y': .35}
            self.add_widget(loginbutton)

            registerbutton = MDFillRoundFlatButton(text="Register", on_press=self.registerbutton)
            registerbutton.size_hint_x = 0.3
            registerbutton.size_hint_y = 0.1
            registerbutton.pos_hint = {'x': .35, 'y': .25}
            self.add_widget(registerbutton)

            image = Image(source='mylogo.png')
            image.size_hint_x = 0.4
            image.size_hint_y = 0.4
            image.pos_hint = {'x': .3, 'y': .5}
            self.add_widget(image)

            self.count_users = Label(text='')
            self.count_users.size_hint_x = 0.1
            self.count_users.size_hint_y = 0.1
            self.count_users.pos_hint = {'x': .8, 'y': .8}
            self.add_widget(self.count_users)


        else:

            image = Image(source='mylogo.png')
            image.size_hint_x = 0.4
            image.size_hint_y = 0.4
            image.pos_hint = {'x': .3, 'y': .5}
            self.add_widget(image)

            loginbutton = MDFillRoundFlatButton(text="Login", on_press=self.loginbutton)
            loginbutton.size_hint_x = 0.2
            loginbutton.size_hint_y = 0.1
            loginbutton.pos_hint = {'x': .4, 'y': .35}
            self.add_widget(loginbutton)

            registerbutton = MDFillRoundFlatButton(text="Register", on_press=self.registerbutton)
            registerbutton.size_hint_x = 0.2
            registerbutton.size_hint_y = 0.1
            registerbutton.pos_hint = {'x': .4, 'y': .20}
            self.add_widget(registerbutton)

            self.count_users = Label(text='')
            self.count_users.size_hint_x = 0.1
            self.count_users.size_hint_y = 0.1
            self.count_users.pos_hint = {'x': .8, 'y': .8}
            self.add_widget(self.count_users)
        self.countusers()




    def countusers(self):

        client = pymongo.MongoClient(
            "mongodb://users:usersall@megglis-shard-00-00.oz019.mongodb.net:27017,megglis-shard-00-01.oz019.mongodb.net:27017,megglis-shard-00-02.oz019.mongodb.net:27017/Accounts?ssl=true&replicaSet=atlas-zb6fyo-shard-0&authSource=admin&retryWrites=true&w=majority")

        db = client.get_database('Accounts')
        records = db.users
        self.count_users.text = f"Users:{records.count_documents({})}"

    def loginbutton(self,instance):
        megg_app.screen_manager.current = 'LoginP'
    def registerbutton(self,instance):
        megg_app.screen_manager.current = 'RegisterP'




class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if platform == 'android':

            self.username = MDTextField(hint_text='Username', icon_right='account', size_hint_x=None, width=800,
                                        pos_hint={"center_x": .5, "center_y": .6})
            self.add_widget(self.username)

            self.password = MDTextField(hint_text='Password', icon_right='eye-off', size_hint_x=None, width=800,
                                        pos_hint={"center_x": .5, "center_y": .5})
            self.password.password = True
            self.add_widget(self.password)

            loginbutton = MDFillRoundFlatButton(text="Login", on_press=self.loginbutton)
            loginbutton.size_hint_x = 0.3
            loginbutton.size_hint_y = 0.1
            loginbutton.pos_hint = {'x': .35, 'y': .35}
            self.add_widget(loginbutton)

            self.showbutton = MDIconButton(icon="", pos_hint={"center_x": .6, "center_y": .51},
                                           on_press=self.show_password)
            self.add_widget(self.showbutton)
            if value == 1:
                self.messagelabel = Label(text='Account Created')
            else:
                self.messagelabel = Label(text='')
            self.messagelabel.size_hint_x = 0.2
            self.messagelabel.size_hint_y = 0.1
            self.messagelabel.pos_hint = {'x': .3, 'y': .7}
            self.add_widget(self.messagelabel)

            self.registerbutton = Button(text="Don't have an account? Create here", background_color=(0, 0, 0, 0),
                                         on_press=self.register)
            self.registerbutton.size_hint_x = 0.1
            self.registerbutton.size_hint_y = 0.1
            self.registerbutton.pos_hint = {'x': .44, 'y': .22}
            self.add_widget(self.registerbutton)


            backbutton = Button(text="<", background_color=(0, 0, 0, 0),
                                         on_press=self.register)
            backbutton.size_hint_x = 0.1
            backbutton.size_hint_y = 0.1
            backbutton.pos_hint = {'x': .0, 'y': .8}
            self.add_widget(backbutton)
        else:

            self.username = MDTextField(hint_text='Username', icon_right='account', size_hint_x=None, width=200,
                                        pos_hint={"center_x": .5, "center_y": .6})
            self.add_widget(self.username)
            self.password = MDTextField(hint_text='Password', icon_right='eye-off', size_hint_x=None, width=200,
                                        pos_hint={"center_x": .5, "center_y": .5})
            self.password.password = True
            self.add_widget(self.password)

            loginbutton = MDFillRoundFlatButton(text="Login", on_press=self.loginbutton)
            loginbutton.size_hint_x = 0.2
            loginbutton.size_hint_y = 0.1
            loginbutton.pos_hint = {'x': .4, 'y': .3}
            self.add_widget(loginbutton)

            self.showbutton = MDIconButton(icon="", pos_hint={"center_x": .6, "center_y": .51},
                                           on_press=self.show_password)
            self.add_widget(self.showbutton)
            if value == 1:
                self.messagelabel = Label(text='Account Created')
            else:
                self.messagelabel = Label(text='')
            self.messagelabel.size_hint_x = 0.2
            self.messagelabel.size_hint_y = 0.1
            self.messagelabel.pos_hint = {'x': .7, 'y': .6}
            self.add_widget(self.messagelabel)

            self.registerbutton = Button(text="Don't have an account? Create here", background_color=(0, 0, 0, 0),
                                         on_press=self.register)
            self.registerbutton.size_hint_x = 0.1
            self.registerbutton.size_hint_y = 0.1
            self.registerbutton.pos_hint = {'x': .44, 'y': .22}
            self.add_widget(self.registerbutton)

            backbutton = Button(text="<",font_size=30, background_color=(0, 0, 0, 0),
                                on_press=self.back)
            backbutton.size_hint_x = 0.1
            backbutton.size_hint_y = 0.1
            backbutton.pos_hint = {'x': .0, 'y': .8}
            self.add_widget(backbutton)


    def back(self,instance):
        megg_app.screen_manager.current = 'WelcomeP'



    def loginbutton(self, instance):

        if self.username.text == '':
            self.messagelabel.text = "Please fill username"
        elif self.password.text == '':
            self.messagelabel.text = "Please fill password"
        else:
            self.messagelabel.text = ''
            client = pymongo.MongoClient(
                "mongodb://users:usersall@megglis-shard-00-00.oz019.mongodb.net:27017,megglis-shard-00-01.oz019.mongodb.net:27017,megglis-shard-00-02.oz019.mongodb.net:27017/Accounts?ssl=true&replicaSet=atlas-zb6fyo-shard-0&authSource=admin&retryWrites=true&w=majority")
            db = client.get_database('Accounts')
            records = db.users
            user = records.find({'username': f'{self.username.text}'})
            password = ''

            if len(list(user)) == 0:
                self.messagelabel.text = "Username not found"

            else:
                key = ''
                user = records.find({'username': f'{self.username.text}'})
                for x in user:
                    password = x['password']
                    salt = x['salt']
                    username = x['username']
                    key = hashlib.pbkdf2_hmac('sha256', self.password.text.encode('utf-8'), salt, 100000)
                if key != password:
                    self.messagelabel.text = "Wrong password"
                else:
                     self.messagelabel.text = "Login approved"
                     global name
                     name = self.username.text

                     self.HomePage = HomePage()
                     screen = Screen(name='HomeP')
                     screen.add_widget(self.HomePage)
                     megg_app.screen_manager.add_widget(screen)

                     megg_app.screen_manager.current = 'HomeP'


    def show_password(self, instance):
        if self.password.password == True:
            self.password.password = False
            self.password.icon_right = 'eye'
        elif self.password.password == False:
            self.password.password = True
            self.password.icon_right = 'eye-off'

    def refresh(self):
        self.messagelabel.text = 'Account Created'

    def register(self, instance):
        megg_app.screen_manager.current = 'RegisterP'


class RegisterPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'android':

            self.email = MDTextField(hint_text='Email', icon_right='email', size_hint_x=None, width=800,
                                     pos_hint={"center_x": .5, "center_y": .7})
            self.add_widget(self.email)

            self.username = MDTextField(hint_text='Username', icon_right='account', size_hint_x=None, width=800,
                                        pos_hint={"center_x": .5, "center_y": .6})
            self.add_widget(self.username)

            self.password = MDTextField(hint_text='Password', icon_right='eye-off', size_hint_x=None, width=800,
                                        pos_hint={"center_x": .5, "center_y": .5})
            self.password.password = True
            self.add_widget(self.password)

            loginbutton = MDFillRoundFlatButton(text="Sign up", on_press=self.signup)
            loginbutton.size_hint_x = 0.3
            loginbutton.size_hint_y = 0.1
            loginbutton.pos_hint = {'x': .35, 'y': .35}
            self.add_widget(loginbutton)

            self.showbutton = MDIconButton(icon="", pos_hint={"center_x": .6, "center_y": .51},
                                           on_press=self.show_password)
            self.add_widget(self.showbutton)

            self.messagelabel = Label(text='')
            self.messagelabel.size_hint_x = 0.2
            self.messagelabel.size_hint_y = 0.1
            self.messagelabel.pos_hint = {'x': .3, 'y': .8}
            self.add_widget(self.messagelabel)

            self.registerbutton = Button(text="Already have an account? Login here", background_color=(0, 0, 0, 0),
                                         on_press=self.login)
            self.registerbutton.size_hint_x = 0.1
            self.registerbutton.size_hint_y = 0.1
            self.registerbutton.pos_hint = {'x': .44, 'y': .22}
            self.add_widget(self.registerbutton)

            backbutton = Button(text="<", font_size=30, background_color=(0, 0, 0, 0),
                                on_press=self.back)
            backbutton.size_hint_x = 0.1
            backbutton.size_hint_y = 0.1
            backbutton.pos_hint = {'x': .0, 'y': .8}
            self.add_widget(backbutton)


        else:
            self.email = MDTextField(hint_text='Email', icon_right='email', size_hint_x=None, width=200,
                                     pos_hint={"center_x": .5, "center_y": .7})
            self.add_widget(self.email)

            self.username = MDTextField(hint_text='Username', icon_right='account', size_hint_x=None, width=200,
                                        pos_hint={"center_x": .5, "center_y": .6})
            self.add_widget(self.username)

            self.password = MDTextField(hint_text='Password', icon_right='eye-off', size_hint_x=None, width=200,
                                        pos_hint={"center_x": .5, "center_y": .5})
            self.password.password = True
            self.add_widget(self.password)

            loginbutton = MDFillRoundFlatButton(text="Sign up", on_press=self.signup)
            loginbutton.size_hint_x = 0.2
            loginbutton.size_hint_y = 0.1
            loginbutton.pos_hint = {'x': .4, 'y': .3}
            self.add_widget(loginbutton)

            self.showbutton = MDIconButton(icon="", pos_hint={"center_x": .6, "center_y": .51},
                                           on_press=self.show_password)
            self.add_widget(self.showbutton)

            self.messagelabel = Label(text='')
            self.messagelabel.size_hint_x = 0.2
            self.messagelabel.size_hint_y = 0.1
            self.messagelabel.pos_hint = {'x': .7, 'y': .6}
            self.add_widget(self.messagelabel)

            self.registerbutton = Button(text="Already have an account? Login here", background_color=(0, 0, 0, 0),
                                         on_press=self.login)
            self.registerbutton.size_hint_x = 0.1
            self.registerbutton.size_hint_y = 0.1
            self.registerbutton.pos_hint = {'x': .44, 'y': .22}
            self.add_widget(self.registerbutton)


            backbutton = Button(text="<", font_size=30, background_color=(0, 0, 0, 0),
                                on_press=self.back)
            backbutton.size_hint_x = 0.1
            backbutton.size_hint_y = 0.1
            backbutton.pos_hint = {'x': .0, 'y': .8}
            self.add_widget(backbutton)

    def back(self, instance):
        megg_app.screen_manager.current = 'WelcomeP'

    def login(self, instance):
        megg_app.screen_manager.current = 'LoginP'

    def signup(self, instance):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if self.email.text == '' and self.username.text == '' and self.password.text == '':
            self.messagelabel.text = 'Please fill the gaps'
        elif self.email.text == '':
            self.messagelabel.text = "Please provide an email"
        elif (re.fullmatch(regex, self.email.text)) == None:
            self.messagelabel.text = "Please provide a correct email"
        elif self.username.text == '':
            self.messagelabel.text = "Please fill username"
        elif len(self.username.text) < 4:
            self.messagelabel.text = 'username must have more than 4 characters'
        elif self.password.text == '':
            self.messagelabel.text = "Please fill password"
        elif len(self.password.text) < 8:
            self.messagelabel.text = 'password must have more than 8 characters'


        else:
            self.messagelabel.text = ''
            client = pymongo.MongoClient(
                "mongodb://users:usersall@megglis-shard-00-00.oz019.mongodb.net:27017,megglis-shard-00-01.oz019.mongodb.net:27017,megglis-shard-00-02.oz019.mongodb.net:27017/Accounts?ssl=true&replicaSet=atlas-zb6fyo-shard-0&authSource=admin&retryWrites=true&w=majority")
            db = client.get_database('Accounts')
            records = db.users
            user = records.find({'username': f'{self.username.text}'})
            if len(list(user)) == 0:
                salt = os.urandom(32)
                key = hashlib.pbkdf2_hmac('sha256', self.password.text.encode('utf-8'), salt, 100000)

                user = {"username": f"{self.username.text}", "email": f"{self.email.text}",
                        "password": key, "salt": salt}
                records.insert_one(user)

                screen = megg_app.screen_manager.get_screen('LoginP')
                megg_app.screen_manager.remove_widget(screen)

                global value
                value = 1
                self.LoginPage = LoginPage()
                screen = Screen(name='LoginP')
                screen.add_widget(self.LoginPage)
                megg_app.screen_manager.add_widget(screen)

                megg_app.screen_manager.current = 'LoginP'
            else:
                print("username exists")

    def show_password(self, instance):
        if self.password.password == True:
            self.password.password = False
            self.password.icon_right = 'eye'
        elif self.password.password == False:
            self.password.password = True
            self.password.icon_right = 'eye-off'


class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_grid()
        self.create_gridlayout()
        self.get_data_from_database()
    def create_grid(self):
        layout = GridLayout(cols=6, spacing=10, size_hint_y=None,pos_hint={'center_x':.5 , 'center_y':.85})

        label1 = Label(text="Home",size_hint_y=None)
        label2 = Label(text="-",size_hint_y=None)
        label3 = Label(text="Guest",size_hint_y=None)
        label4=  Label(text="Prediction",size_hint_y=None)
        label5=  Label(text="Result",size_hint_y=None)


        layout.add_widget(label1)
        layout.add_widget(label2)
        layout.add_widget(label3)
        layout.add_widget(label4)
        layout.add_widget(label5)




        self.add_widget(layout)






    def get_data_from_database(self):
        client = pymongo.MongoClient(
            "mongodb://users:usersall@megglis-shard-00-00.oz019.mongodb.net:27017,megglis-shard-00-01.oz019.mongodb.net:27017,megglis-shard-00-02.oz019.mongodb.net:27017/Predictions?ssl=true&replicaSet=atlas-zb6fyo-shard-0&authSource=admin&retryWrites=true&w=majority")

        db = client.get_database('Predictions')

        records = db.Prediction
        team = records.find().sort("count", -1)
        for x in team:
            home = x['home']
            guest = x['guest']
            prediction = x['prediction']
            score = x['Result']
            color = x['color']

            if color == "0":
                label1 = Label(text=f'{home}',size_hint_y=None, height=15)
                label2 = Label(text='vs',size_hint_y=None, height=15)
                label3 = Label(text=f'{guest}',size_hint_y=None, height=15)
                label4 = Label(text=f'{prediction}',size_hint_y=None, height=15)
                label5 = Label(text=f'{score}',size_hint_y=None, height=15)
                self.layout.add_widget(label1)
                self.layout.add_widget(label2)
                self.layout.add_widget(label3)
                self.layout.add_widget(label4)
                self.layout.add_widget(label5)
            elif color == "2":
                label1 = Label(text=f'{home}', size_hint_y=None, height=15,color = (124/255,252/255,0,1))
                label2 = Label(text='vs', size_hint_y=None, height=15,color = (124/255,252/255,0,1))
                label3 = Label(text=f'{guest}', size_hint_y=None, height=15,color = (124/255,252/255,0,1))
                label4 = Label(text=f'{prediction}', size_hint_y=None, height=15,color = (124/255,252/255,0,1))
                label5 = Label(text=f'{score}', size_hint_y=None, height=15,color = (124/255,252/255,0,1))
                self.layout.add_widget(label1)
                self.layout.add_widget(label2)
                self.layout.add_widget(label3)
                self.layout.add_widget(label4)
                self.layout.add_widget(label5)

            else:
                label1 = Label(text=f'{home}', size_hint_y=None, height=15, color=(1, 0, 0, 1))
                label2 = Label(text='vs', size_hint_y=None, height=15, color=(1, 0, 0, 1))
                label3 = Label(text=f'{guest}', size_hint_y=None, height=15, color=(1, 0, 0, 1))
                label4 = Label(text=f'{prediction}', size_hint_y=None, height=15, color=(1, 0, 0, 1))
                label5 = Label(text=f'{score}', size_hint_y=None, height=15, color=(1, 0, 0, 1))
                self.layout.add_widget(label1)
                self.layout.add_widget(label2)
                self.layout.add_widget(label3)
                self.layout.add_widget(label4)
                self.layout.add_widget(label5)






    def create_gridlayout(self):
        self.layout = GridLayout(cols=5, spacing=40, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.scroll = ScrollView()
        self.scroll.size_hint_x = 1.0
        self.scroll.size_hint_y = 0.8
        self.scroll.pos_hint = {'x': .0, 'y': .0}
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)



if __name__ == "__main__":
    megg_app = PredictionApp()
    megg_app.run()