

import pickle
import secrets
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
from email.message import EmailMessage
EMAIL_SENDER="urikes@gmail.com"
EMAIL_PASSWORD="ajgk bfqs ubkl kyse"

def send_email(email_receiver):
    em = EmailMessage()
    em['from'] = EMAIL_SENDER
    em['to'] = email_receiver
    em['subject'] = 'Reset Password Verification'

    em.set_content(f'Your verification code is  {generate_code()} It will expire in 10 minutes')
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, email_receiver, em.as_string())
        print(f'Sent email to {email_receiver}')

def generate_code():
    """Generate a random code with the specified number of digits."""
    return random.randint(1000, 9999)

def return_email(username,filename):
    usersdict = load_data(filename)
    for person in usersdict.values():
        print(person)
        if person.username == username:
            return person.email
    return "there is an error user not in database"


def generate_salt(length=16):
    # Generate a random salt of the specified length (default is 16)
    return secrets.token_hex(length)

def load_data(filename):
    try:
        with open(filename, 'rb') as file:
            dictionary = pickle.load(file)
        return dictionary
    except FileNotFoundError:
        print("Pickle file not found.")
        return []
    except Exception as e:
        print("Error occurred while loading from pickle:", e)
        return []
    
def save_data(dictionary, filename):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(dictionary, file)
        print("Person objects saved to pickle file successfully.")
    except Exception as e:
        print("Error occurred while saving to pickle:", e)

def hash_password(password, salt):
    # Combine the password and salt
    salted_password = password.decode() +peper+ str(salt)

    # Hash the salted password using SHA-256 algorithm
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

    return hashed_password

