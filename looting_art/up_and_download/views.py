from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotAllowed
from django.shortcuts import render
import os
from django.conf import settings

from .forms import UploadFileForm

import subprocess

COUNTING_SCRIPT = os.path.join(settings.BASE_DIR, 'up_and_download/scripts/counting.py')
INPUT = os.path.join(settings.BASE_DIR, 'up_and_download/data/input.csv')
OUTPUT = os.path.join(settings.BASE_DIR, 'up_and_download/data/output_flagged.csv')
RF_PHRASES = os.path.join(settings.BASE_DIR, 'up_and_download/data/red-flags-phrases-full.csv')
RF_NAMES = os.path.join(settings.BASE_DIR, 'up_and_download/data/red-flags-names-full.csv')

column = ''


def flag(file, col):
    cmd = 'python3 {script} {input} {output} --col {col}' \
          ' --rfphrase {rfphrase} --rfname {rfname}'.format(
        script=COUNTING_SCRIPT, input=file, output=OUTPUT, col=col,
        rfphrase=RF_PHRASES, rfname=RF_NAMES
    )
    subprocess.call(cmd, shell=True)


def returnDownload(file, col):
    with open(INPUT, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    flag(INPUT, col)


# Index.html
def index(request):
    return render(request, 'index.html')


# Upload file and give column to check/flag
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            column = request.POST.get('column')
            returnDownload(request.FILES['testCSV'], column)

            if not os.path.exists(OUTPUT):
                raise HttpResponseServerError

            with open(OUTPUT, 'r') as fh:
                response = HttpResponse(fh.read(), content_type="text/csv")
                response['Content-Disposition'] = 'attachment; filename=test.csv'
                return response
    else:
        return HttpResponseNotAllowed(['POST'])
