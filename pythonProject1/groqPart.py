import smtplib
import os
from email.message import EmailMessage
from groq import Groq

# Groq Client Initialization
api_key = os.getenv("GROQ_API_KEY") 
client = Groq(api_key=api_key)

# function that generates a summary from a text file
def summarize_text_with_groq(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # preparing a message for the Groq model
        messages = [
            {
                'role': 'system',
                'content': 'You are a helpful assistant that summarizes text documents.'
            },
            {
                'role': 'user',
                'content': f'Summarize the following text:\n\n{content}'
            }
        ]

        # Groq API call
        chat_completion = client.chat.completions.create(
            temperature=0.7,
            n=1,
            model="mixtral-8x7b-32768",
            max_tokens=500,
            messages=messages
        )

        # downloading the generated summary content
        summary = chat_completion.choices[0].message.content
        print("Generated summary:", summary)  # debug: print summary
        return summary
    
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None


# function sending an email
def send_email(file_path, recipient_email, subject, body, sender_email, sender_password):
    # generating summary file content 
    summary = summarize_text_with_groq(file_path)
    if not summary:
        print("Failed to generate summary. Email will not be sent.")
        return

    # creating a summary text file
    summary_file_path = "summary.txt"
    with open(summary_file_path, "w", encoding='utf-8') as summary_file:
        summary_file.write(summary)

    # creating an email
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(body)

    # adding the original file and summary as attachments
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_name = file_path.split('/')[-1] 
        msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)
        
        with open(summary_file_path, 'rb') as summary_file:
            summary_file_data = summary_file.read()
        msg.add_attachment(summary_file_data, maintype='text', subtype='plain', filename="summary.txt")
        
    except FileNotFoundError:
        print("File not found!")
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
    file_path='text_to_summarize.txt',
    recipient_email='recipient@gmail.com',
    subject='File with Summary',
    body='The email contains the file and its summary as an attachment.',
    sender_email='your_mail@gmail.com',
    sender_password=os.getenv("EMAIL_PASSWORD")
)
