from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob, random, smtplib, secrets
from datetime import datetime
from pathlib import Path
from email.message import EmailMessage

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            anim = Animation(color = (0.6, 0.7, 0.1, 1))
            anim.start(self.ids.login_wrong)
            self.ids.login_wrong.text = "Wrong username or password!"
    
    def forgot_password(self):
        self.manager.current = "forgot_password"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
            
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right' 
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right' 
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in 
                              available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ForgotPasswordScreen(Screen):
    def reset_password(self, email):
        # check if the email exists in the user database
        self.manager.current = "login_screen"
        with open("users.json") as file:
            users = json.load(file)
        if email in users:
            # generate a random password reset token and store it in the user's record
            reset_token = str(random.randint(100000, 999999))
            users[email]['reset_token'] = reset_token
            with open("users.json", 'w') as file:
                users[email]['reset_token'] = reset_token
                json.dump(users, file)

            # send a password reset email to the user
            sender_email = 'example@gmail.com'
            sender_password = 'password'
            receiver_email = email
            subject = 'Password Reset'
            body = f'Use this token to reset your password: {reset_token}'
            message = f'Subject: {subject}\n\n{body}'
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, receiver_email, message)

            self.manager.current = "reset_password_screen"
        else:
            # anim = Animation(color = (0.6, 0.7, 0.1, 1))
            # anim.start(self.ids.reset_password_wrong)
            self.ids.reset_password_wrong.text = "Email or username not found"

class ResetPasswordScreen(Screen):
    def reset_password(self, email, reset_token, new_password):
        # check if the reset token matches the one stored in the user's record
        with open("users.json") as file:
            users = json.load(file)
        if email in users and 'reset_token' in users[email] and users[email]['reset_token'] == reset_token:
            # update the user's password and remove the reset token
            users[email]['password'] = new_password
            del users[email]['reset_token']
            with open("users.json", 'w') as file:
                json.dump(users, file)

            self.manager.current = "login_screen"
        else:
            anim = Animation(color = (0.6, 0.7, 0.1, 1))
            anim.start(self.ids.reset_password_wrong)
            self.ids.reset_password_wrong.text = "Invalid reset token"

class ResetPasswordWidget:
    def send_reset_link(self, email):
        # generate unique reset password token
        token = secrets.token_hex(32)
        
        # store token in database
        ResetToken.create(token=token, email=email, timestamp=datetime.now())
        
        # send email with reset password link
        msg = EmailMessage()
        msg.set_content('Click the link to reset your password.')
        msg['Subject'] = 'Reset Password'
        msg['From'] = 'noreply@example.com'
        msg['To'] = email
        msg.add_alternative(f'<a href="https://example.com/reset_password?token={token}">Reset Password</a>', subtype='html')
        
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('your_email@example.com', 'your_password')
            smtp.send_message(msg)


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == '__main__':
    MainApp().run()