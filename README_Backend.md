## Install backend on Mac**
Step 3 and 4 are optional.

1. Install Python using command: `brew install python@3.10`
2. After installaton verify with command: `python3 --version`
3. Install Python version management tool pyenv by cloning repo to your home directory: `git clone https://github.com/pyenv/pyenv.git ~/.pyenv`
4. Add it to bashrc:
````
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
````
5. Install python virtual environment and then add folder that is created to .gitignore
python3 -m venv [putNameOfVirtualEnvironmentHere]
6. Run following command to activate virtual enviornment:
source nameOfVirtualEnvironment/bin/activate
7. Change to backend folder via cd backend
8. Run command: `pip3 install -r requirements.txt` to install python packages
9. Create a .env in root of project and add your environment variables to it.

## Run backend server
1. In backend folder run `uvicorn main:app --reload` to start a http server at http://127.0.0.1:8000/.
2. To see the api endpoints go to http://127.0.0.1:8000/docs
3. Now you can change action of forms to local endpoint at http://127.0.0.1:8000/tennis-form and test forms locally.

## Deployment to Deta.sh from a Mac
1. Download deta cli from: https://docs.deta.sh/docs/cli/install
2. Cd to backend folder
3. run: deta login in terminal and it will take you to login page of deta in browser, use credentials in .crendtials.evn to login
4. run: deta update -e .env
5. run: deta deploy

