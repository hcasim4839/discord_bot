**Note: The {} section is meant to not acutally be typed but to input the value that would be appropriate

useful terminal commands:
  - git clone {url}
  - python3.12 -m pip install -r requirements.txt -t .


Clone the repo using the first useful command. The next step is to run the second command to have all the necessary packages installed. If not bot won't run. Also you need the aws credentials which the owner has. Request credentials.


Discord Bot Strucuture

discord-bot/
│
├── bot.py                  # Main bot entry point (initializes client and runs the bot)
├── config.py               # Configuration file for storing token and other settings
├── cogs/                   # Folder for bot "cogs" (extensions) - modular functionality
│   ├── __init__.py         # Allows the cogs folder to be a module
│   ├── events.py           # Handle bot events like on_ready, on_message, etc.
│   ├── commands.py         # Handle bot commands like !help, !ping, etc.
│   └── logging.py          # Handle logging, if needed
│
├── data/                   # Data-related files (e.g., database connections, state)
│   ├── __init__.py         # To make this folder a module
│   ├── database.py         # Logic for interacting with a database (e.g., DynamoDB, SQLite)
│   └── settings.json       # Any persistent state or configuration stored in JSON
│
├── utils/                  # Utility functions (e.g., helpers for commands, logging)
│   ├── __init__.py         # Makes this folder a module
│   ├── helpers.py          # Functions you use across cogs or events
│   └── logging.py          # Custom logging functionality
│
└── requirements.txt        # Python dependencies for the bot
