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
CUSTOM_RF_PHRASES = os.path.join(settings.BASE_DIR, 'up_and_download/data/custom-red-flags-phrases.csv')
RF_PHRASES = os.path.join(settings.BASE_DIR, 'up_and_download/data/red-flags-phrases-full.csv')
RF_NAMES = os.path.join(settings.BASE_DIR, 'up_and_download/data/red-flags-names-full.csv')

column = ''


def flag(file, col, use_custom_indicators=False):
    rfphrase = CUSTOM_RF_PHRASES if use_custom_indicators else RF_PHRASES
    cmd = 'python3 {script} {input} {output} --col {col}' \
          ' --rfphrase {rfphrase} --rfname {rfname}'.format(
        script=COUNTING_SCRIPT, input=file, output=OUTPUT, col=col,
        rfphrase=rfphrase, rfname=RF_NAMES
    )
    check_output(cmd, shell=True)


def process_input_csv(file, col, indicator_file=None):
    custom_indicator = indicator_file is not None
    with open(INPUT, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    if indicator_file is not None:
        with open(CUSTOM_RF_PHRASES, 'wb+') as destination:
            for chunk in indicator_file.chunks():
                destination.write(chunk)
    flag(INPUT, col, custom_indicator)


# Index.html
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def error(request):
    return render(request, 'error.html')


# Upload file and give column to check/flag
def upload_file(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {
            'error_message': 'Wrong file format uploaded. Please try again with a csv file.'
        }
        return render(request, 'error.html', context)

    try:
        indicator_csv = request.FILES.get('indicatorCSV')
        process_input_csv(
            request.FILES['testCSV'],
            request.POST.get('column'),
            indicator_csv
        )
    except CalledProcessError:
        context = {
            'error_message': 'Couldn\'t process the csv file. '
                             'Please make sure the provenance column name is correct and try again.'
        }
        return render(request, 'error.html', context)

    if not os.path.exists(OUTPUT):
        context = {
            'error_message': 'Sorry, something went wrong. Please try again.'
        }
        return render(request, 'error.html', context)

    with open(OUTPUT, 'r') as fh:
        response = HttpResponse(fh.read(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=results.csv'

    # Clean up
    try:
        os.remove(INPUT)
        os.remove(OUTPUT)
        os.remove(CUSTOM_RF_PHRASES)
    except FileNotFoundError:
        pass

    return response
