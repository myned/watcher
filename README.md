# Watcher
An experimental [Hikari](https://www.hikari-py.dev) Discord bot for assigning active and inactive roles based on member activity

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B1AUB66)

## Prerequisites
Linux is used for the following commands\
[WSL](https://docs.microsoft.com/en-us/windows/wsl) can be used to run Linux on Windows, but is not required to run the bot
## Requirements
[Git](https://git-scm.com/downloads)\
[Python](https://www.python.org) 3.10+\
[Poetry](https://python-poetry.org/docs/master)
## Installing
1. Clone repository
```
git clone https://github.com/Myned/Watcher.git
```
2. Go to project folder
```
cd Watcher
```
3. Create a virtual environment and install dependencies
```
poetry install
```
## Usage
1. Go to project folder
```
cd Watcher
```
2. Run with optimizations
```
poetry run python -OO run.py
```
## Setup
Run to create `config.toml`\
The file will automatically generate if it does not exist
```
client = 0 # bot application id
token = "" # bot token
activity = "you" # bot status
db = "watcher.db" # sqlite3 db filepath
guild = 0 # guild id to watch
active = 0 # active role id
inactive = 0 # inactive role id
duration = 0 # time in seconds before considered inactive
```
### systemd service
Run in the background on most Linux machines\
This assumes that the project folder is located at `~/.git/Watcher`\
Change the `WorkingDirectory` path in `watcher.service` if this is not the case
1. Go to project folder
```
cd Watcher
```
2. Copy user service file
```
cp watcher.service ~/.config/systemd/user
```
3. Reload user daemon
```
systemctl --user daemon-reload
```
4. Start and enable service on login
```
systemctl --user enable --now watcher
```
5. Enable lingering to start user services on boot
```
sudo loginctl enable-linger username
```
## Updating
1. Go to project folder
```
cd Watcher
```
2. Pull changes from repository
```
git pull
```
3. Update virtual environment
```
poetry update
```
4. Restart systemd user service
```
systemctl --user restart watcher
```
## Uninstalling
1. Stop and disable systemd user service
```
systemctl --user disable --now watcher
```
2. Remove systemd user service file
```
rm ~/.config/systemd/user/watcher.service
```
3. Optionally disable lingering
```
sudo loginctl disable-linger username
```
4. Remove project folder
```
rm -rf Watcher
```
## Contributing
1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository on GitHub
2. Make changes to the code
3. Format the code with [Black](https://black.readthedocs.io/en/stable) inside the project folder
    ```
    poetry run python black .
    ```
4. [Commit](https://github.com/git-guides/git-commit) the changes to the fork
5. Create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) from the fork
## Credits
[hikari](https://github.com/hikari-py/hikari)\
[hikari-lightbulb](https://github.com/tandemdude/hikari-lightbulb)\
[hikari-miru](https://github.com/HyperGH/hikari-miru)
