# GLAMhack2021 Looted-Art Detector
Go to https://artdata.pythonanywhere.com to use the Looted-Art Detector.

This project was made as part of GLAMhack2021, to deploy the analysis of provenance texts done in
[GLAMhack2020](https://github.com/parisdata/GLAMhack2020) so that anyone can use it online.

Users can upload a csv file with provenance data in it, and receive an output csv that flags artworks whose provenance
should be investigated.

## Running locally
Run 
```
git submodule update --init
pip install -r requirements.txt
pip install -r looting_art/up_and_download/scripts/requirements.txt
```
Then
```
cd looting_art
python3 manage.py runserver
```
Go to http://127.0.0.1:8000/ to test it locally.


## Frontend
![Screenshot of Looted-Art Detector interface](screenshot.jpg?raw=true)
