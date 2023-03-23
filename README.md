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
git clone https://github.com/Myned/watcher.git
```
2. Go to project folder
```
cd watcher
```
3. Create a virtual environment and install dependencies
```
poetry install
```
## Usage
1. Go to project folder
```
cd watcher
```
2. Run with optimizations
```
poetry run python -OO run.py
```
## Setup
### Starting
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
### Inviting
1. Setup a bot application at Discord's [developer portal](https://discord.com/developers/applications)
2. Under General Information, paste `APPLICATION ID` into `config.toml` > `client`
3. Under Bot, click `Add Bot`
4. Under Bot, enable `SERVER MEMBERS INTENT` (necessary for limbo command)
5. Under Bot, paste `TOKEN` into `config.toml` > `token`
6. Under OAuth2 > URL Generator, check `SCOPES` > `bot` and `BOT PERMISSIONS` > `Manage Roles` and `Read Messages/View Channels`
7. Paste generated URL into a browser to invite the bot
### systemd service
Run in the background on most Linux machines\
This assumes that the project folder is located at `~/.git/watcher`\
Change the `WorkingDirectory` path in `watcher.service` if this is not the case
1. Go to project folder
```
cd watcher
```
2. Copy user service file
```
cp watcher.service ~/.config/systemd/user
```
3. Replace `user` in `WorkingDirectory` with current user
```
sed -i "s|\(WorkingDirectory=/home/\)user|\1$(whoami)|" ~/.config/systemd/user/watcher.service
```
4. Reload user daemon
```
systemctl --user daemon-reload
```
5. Start and enable service on login
```
systemctl --user enable --now watcher
```
6. Enable lingering to start user services on boot
```
sudo loginctl enable-linger $(whoami)
```
## Updating
1. Go to project folder
```
cd watcher
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
rm -rf watcher
```
## Contributing
1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository on GitHub
2. Make changes to the code
3. Format the code with [Black](https://black.readthedocs.io/en/stable) inside the project folder
    ```
    poetry run black .
    ```
4. [Commit](https://github.com/git-guides/git-commit) the changes to the fork
5. Create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) from the fork
## Credits
[hikari](https://github.com/hikari-py/hikari)\
[hikari-lightbulb](https://github.com/tandemdude/hikari-lightbulb)\
[hikari-miru](https://github.com/HyperGH/hikari-miru)
