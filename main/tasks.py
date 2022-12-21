from .services import generatePdfFromHtml
from celery import Celery

app = Celery(broker='redis://localhost:6379/0')


@app.task
def generatePdfAsync(pk2):
    generatePdfFromHtml(pk2)