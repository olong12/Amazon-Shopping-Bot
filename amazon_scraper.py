from bs4 import BeautifulSoup
from requests_html import HTMLSession
import os
import time
import smtplib , ssl
import requests

class Scraper:

    #Initializes the scraper shopping bot
    def __init__(self,url,budget,u_email):

        #Attributes about product
        self.url = url
        self.budget = budget

        #Setting user email
        self.u_email = u_email

        #Attributes about scraping
        self.session = HTMLSession()
        # specifying user agent, You can use other user agents
        # available on the internet
        self.HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'})
        # Making the HTTP Request
        print(requests.get(self.url, headers=self.HEADERS))
        self.webpage = requests.get(self.url, headers=self.HEADERS)
        self.parser = 'lxml'
        self.soup = BeautifulSoup(self.webpage.content,self.parser)

    #Prints the object
    def __str__(self):
        return self.soup.prettify()

    #Stores the title of the product
    def get_title(self):
        title = self.soup.find("span",
                attrs={"id": 'productTitle'})
        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        self.product_title = title_value.strip().replace(',', '')
        return self.product_title

    #Stores the price of the product after filtering the string and converting it to an integer
    def get_price(self):
        try:
            price = self.soup.find(
                "span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
            # we are omitting unnecessary spaces
            # and commas form our string
        except AttributeError:
            try:
                price = self.soup.find(id='priceblock_saleprice').get_text().replace('$', '').replace(',', '').strip()
            except:
                try:
                    price = self.soup.find(id='newBuyBoxPrice').get_text().replace('$', '').replace(',', '').strip()
                except:
                    price = 'NA'
        print(price)
        self.product_price = price.strip().replace(',', '')
        if self.product_price[0] == '$':
            self.product_price = self.product_price[1:]
        return self.product_price

    #Prints product title
    def print_title(self):
        print(self.product_title)
        return

    #Prints product price
    def print_price(self):
        print(self.product_price)
        return

    #Checks if the price of the product is below the budget
    def is_below_budget(self):
        if float(self.product_price) <= self.budget:
            return True
        else:
            return False

    #Runs the scraper
    def run(self):
        self.get_title()
        self.get_price()
        self.alert = self.is_below_budget()
        self.status = False
        if self.alert:
            self.status = self.send_email()
        return self.status

    #Sends an email when the condition is satisfied. Under testing!
    def send_email(self):

        #Attributes for email sending
        port = 587
        smtp_server = 'smtp.gmail.com'
        self.email = str(os.environ.get('DEVELOPER_MAIL'))
        self.app_pw = str(os.environ.get('DEVELOPER_PASS'))

        #Message details
        subject = f'The price of {self.get_title()} is within your budget!'

        body_start = 'Hey there!\n\nThe price is now within your budget. Here is the link, buy it now!\n'
        body_mid = self.url
        body_end = '\n\nRegards\nYour friendly neighbourhood programmer'
        body = str(body_start) + str(body_mid) + str(body_end)

        message = f"Subject: {subject}\n\n{body}"

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.email, self.app_pw)
            server.sendmail(self.email, self.u_email, message)
        print("Email sent successfully!")
        self.server.quit()
        return True


def main():
    url = input("Paste the link of the Amazon product whose price you wish to monitor:")
    budget = int(input("Enter you budget price:"))
    u_email = input("Enter your email:")
    inp_str = ("How frequuently would you like to receive updates?"
               "\n1.Every hour\n2.Every 3 hours\n3.Every 6 hours"
               "\nEnter your choice (Default choice is 6 hours):")
    time_choice = int(input(inp_str))
    if time_choice == 1:
        time_delay = 60 * 60
    elif time_choice == 2:
        time_delay = 3 * 60 * 60
    else:
        time_delay = 6 * 60 * 60
    msg = ("Great! Now just sit back and relax. Minimize this program and be sure "
            "that it is running.\nAdditionally, ensure that there is stable internet connection "
            "during the time this program runs.\nIf the price of the product falls within your budget, "
            "you will recieve an email regarding the same and this program will auto-close.\nThank you for using "
            "Amazon-Shopping-Bot's scraper!")
    print(msg)
    shopbot = Scraper(url,budget,u_email)
    while True:
        if shopbot.run():
            break
        time.sleep(time_delay)

if __name__ == '__main__':
    main()
