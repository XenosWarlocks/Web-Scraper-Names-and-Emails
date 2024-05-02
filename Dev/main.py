# main.py
from scraper import Scraper

def main():
    url = input("Please provide the URL you'd like to visit: ")
    scraper = Scraper(url)
    names_emails = scraper.scrape()
    with open("name.txt", "w") as name_file, open("email.txt", "w") as email_file:
        for name, email in names_emails:
            if name:
                name_file.write(name + "\n")
            if email:
                email_file.write(email + "\n")
    print("Names and emails have been written to files.")

if __name__ == "__main__":
    main()
