# GLAMhack2021 Looted-Art Detector
This project was made as part of GLAMhack2021, to deploy the analysis of provenance texts done in
[GLAMhack2020](https://github.com/parisdata/GLAMhack2020) so that anyone can use it online.

Users can upload a csv file with provenance data in it, and receive an output csv that flags artworks whose provenance
should be investigated.

## How to use it
Run 
```
pip install -r requirements.txt
```
Then
```
cd looting_art_prototype 
```
Then
```
python3 manage.py migrate
python3 manage.py runserver
```

Go to http://127.0.0.1:8000/ to tests it locally.

## Pitfalls and warning
There are no input/security checks done, so do not use it in productive more just yet.
It currently uses the counting.py file from another project (in parent folder), so if that is updated, you have to copy paste the code in this prototype and wother case adapt the code...

## Frontend (so far)
![Alt text](/looting_art/screenshot.jpg?raw=true)
