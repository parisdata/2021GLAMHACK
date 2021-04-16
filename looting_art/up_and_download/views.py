from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseServerError, HttpResponseNotAllowed
from django.shortcuts import render
import os
from django.conf import settings

from .forms import UploadFileForm

from subprocess import check_output, CalledProcessError

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
    check_output(cmd, shell=True)


def process_input_csv(file, col):
    with open(INPUT, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    flag(INPUT, col)


# Index.html
def index(request):
    return render(request, 'index.html')


# Upload file and give column to check/flag
def upload_file(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest('Please upload a csv file')

    try:
        process_input_csv(
            request.FILES['testCSV'],
            request.POST.get('column')
        )
    except CalledProcessError:
        return HttpResponseBadRequest(
            'Couldn\'t process the csv file. '
            'Please make sure the provenance column name is correct and try again')

    if not os.path.exists(OUTPUT):
        return HttpResponseServerError('Something went wrong')

    with open(OUTPUT, 'r') as fh:
        response = HttpResponse(fh.read(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=test.csv'

    # Clean up
    os.remove(INPUT)
    os.remove(OUTPUT)

    return response
