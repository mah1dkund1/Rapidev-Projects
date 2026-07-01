import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TerminalConsumer(AsyncWebsocketConsumer) :
    async def connect(self):

        await self.channel_layer.group_add("scraper_group", self.channel_name)
        await self.accept()
        print("\n[WS LINKED] A client has connected to the terminal stream pipeline!\n")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("scraper_group", self.channel_name)
        print("\n[WS UNLINKED] A client disconnected from the stream.\n")
    

    async def send_scrapper_update(self, event):
        quote_data = event['text']


        #printing the scraped data to the terminal for now, web page view will be made later

        print("\n==================================================")
        print(f"[REAL-TIME SIGNAL EVENT RECEIVED]")
        print(f"Author/Title: {quote_data.get('title')}")
        print(f"Quote Value:  {quote_data.get('value')}")
        print("==================================================\n")
        
        
        await self.send(text_data=json.dumps(quote_data))
        


