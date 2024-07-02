## LanguageLoop Telegram Bot 

This project implements a Telegram bot that assists users in learning a language fluently. It leverages OpenAI's gpt-4o model for conversation generation and feedback mechanisms.

### Features

* **Interactive Language Learning:** The bot engages users in conversations, asking questions tailored to their chosen language and skill level.
* **Grammar Correction:** The bot analyzes user responses, identifies grammatical errors, and provides explanations for improvement.
* **Natural Conversation Flow:** The bot strives to maintain a natural conversation, building upon previous responses and topics discussed.
* **Audio Transcription and Feedback:** Supports audio input (voice messages) through transcription and feedback on the transcribed text. 
* **Text-to-Speech Output:** Converts generated responses to audio for an immersive learning experience.

### Requirements

To run this project, you'll need the following:

* Python 3.x
* The following Python libraries (listed in [requirements.txt](requirements.txt)):
    * openai
    * python-telegram-bot
    * python-dotenv

### Installation

1. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```
2. Rename `.env.template` to `.env` and fill in your OpenAI API key and Telegram Bot token:

   ```
   LANGUAGE_LOOP_TELEGRAM_BOT_TOKEN=<your_api_key>
   OPENAI_API_KEY=<your_api_key>
   ```

### Running the Bot

1. Save your changes to the `.env` file.
2. Run the following command from the project directory:

   ```bash
   python telegram_bot.py
   ```

This will start the bot and allow users to interact with it on Telegram.

### Usage

1. Add the LanguageLoop bot to your Telegram contacts by searching for its username (which will be generated based on your Telegram Bot token).
2. Start a conversation with the bot by sending the `/start` command.
3. The bot will guide you through initial setup, including selecting your target language and proficiency level.
4. Respond to the bot's questions and prompts to engage in the language learning process.
5. The bot will provide feedback on your grammar and guide you towards fluency.

### Additional Notes

* The `prompt.py` file defines initial instructions for the bot's behavior.
* The `db.py` file manages user data persistence using a SQLite database.
* This is a basic implementation, and future improvements might include:
    * Support for multiple languages
    * More advanced conversation topics
    * Integration with additional language learning resources

Contributions are welcome!
