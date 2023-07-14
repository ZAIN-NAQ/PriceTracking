import requests
from bs4 import BeautifulSoup
import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def compare_price():
    """This Function Compares the price of the product with my budget"""
    try:
        url="https://www.next.co.uk/style/st518445/230742#230742"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_name_element=soup.find('div',{ 'class':'Title'})
        product_name= product_name_element.find('h1').text.strip()
        product_price_element=soup.find('div',{ 'class':'nowPrice branded-markdown'})
        product_price = product_price_element.find('span').text
        product_price = float(product_price.replace('£', ''))
        
        #My Budget 
        budget= 50 

        if product_price <= budget:
            print("Yes the product is in range")
            send_email(product_name,product_price)
    except Exception as e:
        print('The scraping job failed !')
        print(e)  

def send_email(product_name,product_price):
    try:
        sender_email = 'zainhyder34@outlook.com'  # Replace with your email address
        receiver_email = 'zainhyder34@gmail.com'  # Replace with the email address to receive notifications
        # Securely input email password
        password = getpass.getpass('Enter your email password: ')
        subject = 'Price Drop Alert!'
        body = f"The price of '{product_name}' has dropped to £{product_price}. Check it out now!"
       
        # Create the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        # Encode the subject with UTF-8 using the email.header module
        subject_encoded = Header(subject, 'utf-8').encode()

        # Set the encoded subject in the email message
        message['Subject'] = subject_encoded

        # Attach the body to the email
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        # Login to your email account
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Close the connection
        server.quit()
    except Exception as e:
        print('Email Job Failed')
        print(e)

compare_price()
