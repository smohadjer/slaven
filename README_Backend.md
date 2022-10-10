Site hosted on GitHub via GitHub Pages at:
https://smohadjer.github.io/slaven/

Running backend on localhost on Mac
1. Install Python using command: brew install python@3.10
2. After installaton verify with command: python3 --version
3. Install Python version management tool pyenv by cloning repo to your home directory: git clone https://github.com/pyenv/pyenv.git ~/.pyenv
4. Add it to bashrc:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc

