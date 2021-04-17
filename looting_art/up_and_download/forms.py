from django import forms
from upload_validator import FileTypeValidator


class UploadFileForm(forms.Form):
    column = forms.CharField(label='column', max_length=100)
    testCSV = forms.FileField(
        validators=[FileTypeValidator(
            allowed_types=['text/csv', 'text/plain']
        )]
    )
    indicatorCSV = forms.FileField(
        validators=[FileTypeValidator(
            allowed_types=['text/csv', 'text/plain']
        )],
        required=False
    )
