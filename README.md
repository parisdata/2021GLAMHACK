# GLAMhack2021 Looted-Art Detector
This project was made as part of GLAMhack2021, to deploy the analysis of provenance texts done in
[GLAMhack2020](https://github.com/parisdata/GLAMhack2020) so that anyone can use it online.

Users can upload a csv file with provenance data in it, and receive an output csv that flags artworks whose provenance
should be investigated.

## How to use it
Run 
```
git submodule update --init
pip install -r requirements.txt
pip install -r looting_art_prototype/up_and_download/GLAMhack2020/requirements.txt
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

## Frontend (so far)
![Alt text](/looting_art/screenshot.jpg?raw=true)
