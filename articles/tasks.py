from celery import shared_task
from fetch_articles import delete_old_entries, list_yesterdays_entries

@shared_task
def update_articles():
    delete_old_entries()
    list_yesterdays_entries()
