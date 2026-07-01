from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ScrapedData

@receiver(pre_save, sender=ScrapedData)

def clean_scraped_data(sender, instance, **kwargs):
    if instance.title:
        instance.title = instance.title.strip()

    if instance.value:
        instance.value = instance.value.strip()

    print(f"[PRE-SAVE] Data for '{instance.title}' sanitized successfully.")    



@receiver(post_save, sender=ScrapedData)

def broadcast_scraped_data(sender, instance, created, **kwargs):
    if created: 
        channel_layer = get_channel_layer()

        payload = {
            "title": instance.title,
            "value": instance.value
        }

        async_to_sync(channel_layer.group_send)(
            "scraper_group" ,
            {
                "type": "send_scraper_update",
                "text": payload

            }
        )

        print(f"[POST-SAVE] Live broadcast dispatched for tracking entry.")


# ... all your existing signal code here ...

print("\n>>> CRITICAL: status/signals.py has been READ by Python! <<<\n")
