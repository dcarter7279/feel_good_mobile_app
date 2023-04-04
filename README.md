# feel_good_mobile_app
This code is a Python program that uses the Kivy framework to create a simple login system with password reset functionality. It includes five screens: LoginScreen, SignUpScreen, SignUpScreenSuccess, LoginScreenSuccess, ForgotPasswordScreen, and ResetPasswordScreen.

The LoginScreen screen allows the user to enter their username and password. If the entered credentials are correct, the user will be directed to the LoginScreenSuccess screen. Otherwise, an error message will be displayed.

The SignUpScreen screen allows the user to create a new account by entering their desired username and password. The user's information will be stored in a JSON file called "users.json". After the user account is created, the SignUpScreenSuccess screen will be displayed.

The LoginScreenSuccess screen displays a welcome message and allows the user to log out or get a quote based on their current mood.

The ForgotPasswordScreen screen allows the user to reset their password by entering their email address. If the entered email address exists in the user database, a password reset email will be sent to the user's email address. The email contains a reset token that the user can use to reset their password.

The ResetPasswordScreen screen allows the user to enter their email address, the reset token, and a new password to reset their password. If the reset token is valid and matches the token stored in the user database, the user's password will be updated with the new password.

The program uses the glob, json, random, secrets, smtplib, pathlib, datetime, hoverable, image, and behaviors modules in Python. It also loads the design.kv file, which contains the design elements for the screens.

Note: the ResetPasswordWidget class is not used in the program and can be ignored.
