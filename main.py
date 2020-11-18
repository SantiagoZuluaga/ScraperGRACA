import os
from dotenv import load_dotenv
from scraper.scraper import Scraper

def main():
    load_dotenv()
    email = os.environ.get('EMAIL_USER')
    password = os.environ.get('PASSWORD_USER')
    scraper = Scraper(email, password)
    scraper.login()
    scraper.getEstudiantes('Ingenieria')

if __name__ == "__main__":
    main()