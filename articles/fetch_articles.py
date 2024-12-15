import os
import feedparser
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import sqlite3
import re
import pytz
import requests
from dotenv import load_dotenv

# Ensure db-data folder exists
DB_FOLDER = 'db-data'
DB_PATH = os.path.join(DB_FOLDER, 'articles.db')
os.makedirs(DB_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist

def initialize_database():
    """Ensures the database and table exist."""
    conn = sqlite3.connect(DB_PATH)  # Save to db-data/articles.db
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal TEXT,
            journal_url TEXT,
            published_date TEXT,
            title TEXT,
            authors TEXT,
            affiliations TEXT,
            abstract TEXT,
            doi TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized and table ensured.")

JOURNAL_URLS = {
    "Nature Reviews Materials": "https://www.nature.com/natrevmats/",
    "Nature Materials": "https://www.nature.com/nmat/",
    "Materials Today": "https://www.materialstoday.com/",
    "Advanced Materials": "https://onlinelibrary.wiley.com/journal/15214095",
    "Progress in Materials Science": "https://www.journals.elsevier.com/progress-in-materials-science",
    "Nature Nanotechnology": "https://www.nature.com/nnano/",
    "Nano Today": "https://www.journals.elsevier.com/nano-today",
    "Advanced Energy Materials": "https://onlinelibrary.wiley.com/journal/16146840",
    "Chemical Society Reviews": "https://pubs.rsc.org/en/journals/journal/cs",
    "Accounts of Chemical Research": "https://pubs.acs.org/journal/achre4",
    "Acta Materialia": "https://www.journals.elsevier.com/acta-materialia",
    "Scripta Materialia": "https://www.journals.elsevier.com/scripta-materialia",
    "Metallurgical and Materials Transactions A": "https://link.springer.com/journal/11661",
    "Metallurgical and Materials Transactions B": "https://link.springer.com/journal/11663",
    "Computational Materials Science": "https://www.journals.elsevier.com/computational-materials-science",
    "Modelling and Simulation in Materials Science and Engineering": "https://iopscience.iop.org/journal/0965-0393",
    "Advanced Functional Materials": "https://onlinelibrary.wiley.com/journal/16163028",
    "Functional Materials Letters": "https://www.worldscientific.com/worldscinet/fml",
    "Energy & Environmental Science": "https://pubs.rsc.org/en/journals/journal/ee",
    "Journal of Materials Chemistry A": "https://pubs.rsc.org/en/journals/journal/ma",
    "International Journal of Hydrogen Energy": "https://www.journals.elsevier.com/international-journal-of-hydrogen-energy",
    "Corrosion Science": "https://www.journals.elsevier.com/corrosion-science",
    "Steel Research International": "https://onlinelibrary.wiley.com/journal/1869344x",
}


JOURNAL_FEEDS = {
    "Nature Reviews Materials": "https://www.nature.com/natrevmats.rss",
    "Nature Materials": "https://www.nature.com/nmat.rss",
    "Materials Today": "https://www.materialstoday.com/rss/",
    "Advanced Materials": "https://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1521-4095",
    "Progress in Materials Science": "https://www.journals.elsevier.com/progress-in-materials-science/rss",
    "Nature Nanotechnology": "https://www.nature.com/nnano.rss",
    "Nano Today": "https://www.journals.elsevier.com/nano-today/rss",
    "Advanced Energy Materials": "https://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1614-6840",
    "Chemical Society Reviews": "https://pubs.rsc.org/en/journals/rss?journal=cs",
    "Accounts of Chemical Research": "https://pubs.acs.org/page/achre4/feed",
    "Acta Materialia": "https://www.journals.elsevier.com/acta-materialia/rss",
    "Scripta Materialia": "https://www.journals.elsevier.com/scripta-materialia/rss",
    "Metallurgical and Materials Transactions A": "https://www.springer.com/journal/11661",
    "Metallurgical and Materials Transactions B": "https://link.springer.com/journal/11663",
    "Computational Materials Science": "https://www.journals.elsevier.com/computational-materials-science/rss",
    "Modelling and Simulation in Materials Science and Engineering": "https://iopscience.iop.org/journal/0965-0393",
    "Advanced Functional Materials": "https://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1616-3028",
    "Functional Materials Letters": "https://www.worldscientific.com/worldscinet/fml",
    "Energy & Environmental Science": "https://pubs.rsc.org/en/journals/rss?journal=ee",
    "Journal of Materials Chemistry A": "https://pubs.rsc.org/en/journals/rss?journal=ma",
    "International Journal of Hydrogen Energy": "https://www.journals.elsevier.com/international-journal-of-hydrogen-energy/rss",
    "Corrosion Science": "https://www.journals.elsevier.com/corrosion-science/rss",
    "Steel Research International": "https://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1869-344X",
}

def fetch_details_from_crossref(doi, journal_name=None):
    """
    Fetch details from CrossRef for a given DOI and optionally include journal-specific logic.
    """
    url = f'https://api.crossref.org/works/{doi}'
    load_dotenv()
    headers = {'User-Agent': os.getenv('USER_AGENT')}
    #headers = {'User-Agent': 'AMaterialisticBot/0.1 (mailto:omerbuyukuslu@gmail.com)'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        message = data.get('message', {})
        
        # Extract abstract
        abstract = message.get('abstract', '')
        if abstract:
            abstract = re.sub(r'<[^>]+>', '', abstract).strip()
            if abstract.upper().startswith('ABSTRACT'):
                abstract = abstract[8:].strip()
        
        # Extract authors and affiliations
        authors = []
        affiliations = set()
        author_list = message.get('author', [])
        for author in author_list:
            given = author.get('given', '')
            family = author.get('family', '')
            full_name = f"{given} {family}".strip()
            authors.append(full_name)
            affiliation_list = author.get('affiliation', [])
            for affil in affiliation_list:
                affil_name = affil.get('name', '')
                if affil_name:
                    affiliations.add(affil_name)
        
        authors_str = ', '.join(authors)
        affiliations_str = '; '.join(affiliations)

        # Optionally process based on journal-specific logic
        if journal_name:
            print(f"Processed article for journal: {journal_name}")
        
        return abstract, authors_str, affiliations_str
    else:
        print(f"Failed to fetch details for DOI {doi}: {response.status_code}")
        return '', '', ''


def save_entries_to_database(entries):
    """
    Saves articles to the database, ensuring no duplicates based on title.
    Adds journal URLs based on the JOURNAL_URLS dictionary.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure the table exists
    initialize_database()

    for entry in entries:
        # Retrieve the journal URL
        journal_url = JOURNAL_URLS.get(entry['journal'], None)

        # Check for duplicates based on the title
        cursor.execute('SELECT COUNT(*) FROM articles WHERE title = ?', (entry['title'],))
        count = cursor.fetchone()[0]
        if count == 0:  # Only insert if the title does not exist
            cursor.execute('''
                INSERT INTO articles (
                    journal,
                    journal_url,
                    published_date,
                    title,
                    authors,
                    affiliations,
                    abstract,
                    doi
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry['journal'],
                journal_url,
                entry['published_date'],
                entry['title'],
                entry['authors'],
                entry['affiliations'],
                entry['abstract'],
                entry['doi']
            ))
        else:
            print(f"Duplicate found, skipping entry: {entry['title']}")
    
    conn.commit()
    conn.close()
    print(f"Saved {len(entries)} articles to the database (excluding duplicates).")


def delete_old_entries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure the table exists
    initialize_database()

    thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat()  # Change to 30 days

    cursor.execute('''
        DELETE FROM articles WHERE published_date < ?
    ''', (thirty_days_ago,))
    conn.commit()

    rows_deleted = cursor.rowcount
    conn.close()
    print(f"Deleted {rows_deleted} articles older than 30 days.")

def list_yesterdays_entries():
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    today_date = now_utc.date()
    yesterday_date = today_date - timedelta(days=1)
    yesterday_start = datetime.combine(yesterday_date, datetime.min.time()).replace(tzinfo=pytz.utc)
    today_start = datetime.combine(today_date, datetime.min.time()).replace(tzinfo=pytz.utc)

    print(f"Yesterday starts at: {yesterday_start}")
    print(f"Yesterday ends at: {today_start}\n")

    entries_to_save = []

    # Loop through all journals in the feed dictionary
    for journal_name, feed_url in JOURNAL_FEEDS.items():
        print(f"Fetching articles for {journal_name}...")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            title = entry.get('title', 'No Title')
            date_str = entry.get('published') or entry.get('updated') or entry.get('pubDate', 'No Date')
            if date_str == 'No Date':
                continue
            try:
                published = date_parser.parse(date_str)
                if published.tzinfo is None:
                    published = published.replace(tzinfo=pytz.utc)
                else:
                    published = published.astimezone(pytz.utc)
                if yesterday_start <= published < today_start:
                    doi = entry.get('dc_identifier', '')
                    if doi.startswith('doi:'):
                        doi = doi[4:]
                    else:
                        link = entry.get('link', '')
                        match = re.search(r'doi\.org/(10\.\d{4,9}/[-._;()/:A-Z0-9]+)', link, re.I)
                        if match:
                            doi = match.group(1)
                    abstract = ''
                    authors = ''
                    affiliations = ''
                    if doi:
                        abstract, authors, affiliations = fetch_details_from_crossref(doi, journal_name=journal_name)
                    else:
                        print(f"DOI not found for '{title}'")
                    article_entry = {
                        'journal': journal_name,  # Include the journal name
                        'published_date': published.isoformat(),
                        'title': title,
                        'authors': authors,
                        'affiliations': affiliations,
                        'abstract': abstract,
                        'doi': doi
                    }
                    entries_to_save.append(article_entry)
                    print(f"Found article: {title}")
            except Exception as e:
                print(f"Error processing '{title}': {e}")
                continue

    if entries_to_save:
        save_entries_to_database(entries_to_save)
    else:
        print("No articles published yesterday.")


if __name__ == '__main__':
    delete_old_entries()
    list_yesterdays_entries()
