import smtplib
from email.message import EmailMessage

def send_email(file_path, recipient_email, subject, body, sender_email, sender_password):
    
    # creating an email
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(body)
    
    # adding an attachment
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_name = file_path.split('/')[-1]  # getting filename
        msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)
    except FileNotFoundError:
        print("Nie znaleziono pliku!")
        return
    
    # sending email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # connection encryption
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("The email has been sent!")
    except Exception as e:
        print(f"Error sending email: {e}")

# sample use
send_email(
    file_path='example.txt',
    recipient_email='recipent@gmail.com',
    subject='sample subject',
    body='the email attachment contains a brief summary of the meeting in a txt file',
    sender_email='kondziolkaptr@gmail.com',
    sender_password='app_password' ### przerobic na ENV 
)

# print(os.getcwd())
