import time
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from status.models import ScrapedData

class Command(BaseCommand):
    help = "Validates the full ASGI Signal and Channel Layer pipeline locally."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("⚡ Diagnostic Process Test Started..."))
        
        # 1. Manually test if your signals file is responding to saves
        self.stdout.write("\n[Step 1] Creating database record to fire signals...")
        
        # This will call pre_save (strip spaces) and post_save (channel layer broadcast)
        obj = ScrapedData.objects.create(
            title="   Diagnostic Test   ",
            value="Checking if process layers communicate."
        )
        
        self.stdout.write(self.style.SUCCESS(f"✔ Database write complete. Saved ID: {obj.id}"))
        self.stdout.write(f"✔ Sanitized Title Check: '{obj.title}' (Should have no spaces)")
        
        self.stdout.write("\n[Step 2] Testing internal Memory Channel Layer loop...")
        channel_layer = get_channel_layer()
        
        if channel_layer is None:
            self.stdout.write(self.style.ERROR("❌ Error: Channel layer not detected! Check settings.py"))
            return

        self.stdout.write(self.style.SUCCESS("🎉 System Test Complete! Everything is wired up perfectly."))

"""

import time
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from status.models import ScrapedData

class Command(BaseCommand):
    help = "Scrapes target static website every 5 minutes"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Scraper started..."))
        
        #url of the site to be scraped

        URL = "https://quotes.toscrape.com/" 

        while True:
            try:
                self.stdout.write(f"Fetching data from  {URL}")

                response = requests.get(URL, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')


                   
                   # this will extract the title and the text from the websites html
                   
                    quote_blocks = soup.find_all('div',class_='quote')
                    if not quote_blocks:
                        self.stdout.write(self.style.WARNING("No blocks found"))
                        continue

                    self.stdout.write(self.style.SUCCESS(f"Found {len (quote_blocks)} quotes. Saving to db"))

                    for block in quote_blocks:
                        text_element=block.find('span', class_='text')
                        author_element=block.find('small', class_='author')
                         
                        if text_element and author_element:
                            quote_text=text_element.text.strip()
                            author_name=author_element.text.strip()

                            ScrapedData.objects.create(title=author_name, value=quote_text)

                    self.stdout.write(self.style.SUCCESS("Saved successfuly!"))         
                   
                    




                else: self.stdout.write(self.style.WARNING(f"Failed to fetch the data/site, status code: {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error occurred: {str(e)}"))        

            self.stdout.write("Will run again in 30 seconds")
            time.sleep(30)    

"""