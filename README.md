# Reflect

Reflect is a Discord bot written in Python that comes with a variety of useful features, such as animated emojis without Nitro, reaction roles, YouTube search, text filtering and more.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

Reflect has many features. Here are some I love:

- **Animated Emojis Without Nitro:** Users can use animated emojis without needing a Nitro subscription.
- **Reaction Roles:** Server owners can set up reaction roles to allow users to self-assign roles.
- **YouTube Search:** Users can search for YouTube videos watch them directly in Discord.
- **Text Filter:** Reflect has a preconfigured text filter to automatically remove messages containing certain words or phrases.

## Installation

To use Reflect, you will need to have Python 3.6 or higher installed on your machine. You will also need to create a new Discord bot and invite it to your server. To do this, follow these steps:

1. Create a new Discord bot at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Generate a bot token and copy it to your clipboard.
3. Invite the bot to your server.
4. Clone the Reflect repository to your local machine.
5. Create a virtual environment and activate it.
6. Install the required dependencies by running `pip install -r requirements.txt`.

## Usage

1. To use Reflect, first create a new `.env` file in the root of your project directory and add the following lines:

```
BOT_TOKEN=<YOUR_BOT_TOKEN>
YOUTUBE_API_KEY=<YOUR_YOUTUBE_DATA_API_KEY>
MONGO_DB_URI=<MONGODB_URI>
REFLECT_GUILD_ID=0
```

2. Replace the placeholders.
3. To start the bot, simply run `python run.py` in your terminal.

## Contributing

Contributions are welcome! If you have any suggestions for new features, bug fixes, or improvements to the code, please open an issue or submit a pull request.

## License

Reflect is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
