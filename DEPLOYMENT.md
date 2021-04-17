## First deployment on pythonanywhere
These steps are only necessary when deploying for the first time, or if you want to wipe out the old deployed site and 
deploy entirely fresh. (That shouldn't be the case unless the deployed site has got really messed up.) Adapted from the
[DjangoGirls tutorial](https://tutorial.djangogirls.org/en/deploy/) — see their page for more help.

- Log into pythonanywhere
- If it's really the first deployment, create an API token: go to Account, then select the API Token tab, and then click
  the button to create a new token
- Open a Bash console
- Install the pythonanywhere tool:
	```
	pip3.8 install --user pythonanywhere
	```
- Run the tool to automatically configure the app:
	```
	pa_autoconfigure_django.py --python=3.8 https://github.com/parisdata/2021GLAMHACK.git
	```
- Update the scripts folder:
	```
	git submodule update --init
	```
- Go to the Web tab in pythonanywhere and click the green button to reload the app

## How to update
- Log into pythonanywhere and open a Bash console
- Go to the project directory and pull the current git state:
	```
	cd artdata.pythonanywhere.com
	git checkout main
	git pull
	```
- **Care:** there are some changes to the files that are specific to the pythonanywhere deployment. We need to keep
  those changes here, and we also need to not commit them and push them to Github. These changes are in 
  `looting_art/looting_art/settings.py`:
	```
	DEBUG = False

	ALLOWED_HOSTS = ['artdata.pythonanywhere.com']
	```
- The scripts for analysis are found in the folder `looting_art/up_and_download/scripts`, and on GitHub at 
  https://github.com/parisdata/GLAMhack2020. If there have been any changes to the scripts, update them on the server 
  like this:
	```
	git submodule update
	```
- Update the static files (images, JS, CSS):
	```
	python looting_art/manage.py collectstatic
	```
- Go to the Web tab in pythonanywhere and click the green button to reload the app
- If anything is not working, look in the pythonanywhere logs and at the source code (both linked from the Web tab) to
  debug the app

## How to update the scripts
The analysis scripts are located in `looting_art/up_and_download/scripts` (currently, only `counting.py` is used by the
website). If there is an update to the script repo at https://github.com/parisdata/GLAMhack2020, you need to update
the submodule in this repo:
```
cd looting_art/up_and_download/scripts
git checkout master && git pull
```
Then go back to this folder, commit the change and push it. Once the change has been pushed to GitHub, update the
website as described above.

## How to update the red-flag files
The red-flag files are located in `looting_art/up_and_download/data`. Make any changes necessary, commit and push to the
`main` branch, and then update the website as described above.
