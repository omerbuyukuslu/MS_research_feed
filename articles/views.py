from django.shortcuts import render
from .models import Article
import json
from django.http import HttpResponse
import subprocess
from django.http import JsonResponse
from .models import LastUpdated
from django.http import StreamingHttpResponse


def homepage(request):
    return render(request, 'articles/homepage.html')


def article_feed(request):
    articles = Article.objects.all()
    data = [
        {
            "title": article.title,
            "authors": article.authors,
            "journal": article.journal,
            "journal_url": article.journal_url,  
            "published_date": article.published_date.date().isoformat() if article.published_date else None,
            "doi": article.doi,
            "abstract": article.abstract,
        }
        for article in articles
    ]
    return HttpResponse(json.dumps(data), content_type="application/json")

def update_articles(request):
    try:
        # Execute the fetch_articles.py script
        subprocess.run(['python', 'articles/fetch_articles.py'], check=True)

        # Update the last updated timestamp
        LastUpdated.objects.update_or_create(id=1, defaults={})

        return JsonResponse({'status': 'success', 'message': 'Articles updated successfully!'})
    except subprocess.CalledProcessError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

    

def get_last_updated(request):
    try:
        last_updated = LastUpdated.objects.last()
        if last_updated:
            return JsonResponse({'last_updated': last_updated.timestamp.strftime("%Y-%m-%d %H:%M:%S")})
        else:
            return JsonResponse({'last_updated': "Not updated yet"})
    except Exception as e:
        return JsonResponse({'last_updated': "Error retrieving last updated time", 'error': str(e)})

    
from django.http import StreamingHttpResponse
import subprocess
import logging

logger = logging.getLogger(__name__)

def stream_output(request):
    def run_script():
        try:
            process = subprocess.Popen(
                ['python', '-u', 'articles/fetch_articles.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Stream stdout line by line
            for line in process.stdout:
                yield f"data: {line.strip()}\n\n"

            # Stream stderr line by line
            for line in process.stderr:
                yield f"data: ERROR: {line.strip()}\n\n"

            process.wait()

            # Send completion message
            if process.returncode == 0:
                yield "data: Script completed successfully.\n\n"
            else:
                yield f"data: Script failed with return code {process.returncode}.\n\n"

        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"

        # Explicitly send a "done" event to signal completion
        yield "event: done\ndata: Process completed\n\n"

    response = StreamingHttpResponse(run_script(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # Optional for reverse proxies like Nginx
    return response
