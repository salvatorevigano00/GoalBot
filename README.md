**GoalBot**

This Discord bot is designed to facilitate user engagement by allowing them to choose from randomly selected images of Serie A soccer players. It aims to introduce an element of fun and interactivity within the Discord community.

**Usage Instructions**

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and add the bot token:
   ```
   TOKEN=YOUR_BOT_TOKEN
   ```
3. Run the bot:
   ```bash
   python main.py
   ```

**Commands:**

- `!kd`: Generate 3 random images of Serie A soccer players.
- `!kc`: Display the user's collection of players.
- `!kcd`: Display the remaining time for grab and drop.

**Additional Info:**

- Users must wait a cooldown period (5 minutes for grab and 10 minutes for drop) before using the bot again to prevent spamming.
- When grabbing an image, users can select their preferred player by reacting to the displayed images. However, once a player is chosen by any user, it becomes unavailable for others.
- The bot maintains a collection of users' chosen players using JSON as a persistent storage mechanism.
- This project is primarily developed using Python 3.8 and Discord.py, and it leverages the OpenAI GPT-3.5 language model for chat capabilities.
- Users are encouraged to contribute to this open-source project on GitHub (insert GitHub repository link) by reporting bugs, suggesting features, or providing code contributions.
- The project is licensed under the MIT License.
- For detailed information on the bot and its features, please refer to the `main.py`, `moderation.py`, and `carte.py` files in the project repository.
