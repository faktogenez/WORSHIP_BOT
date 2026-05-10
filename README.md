# Telegram Radio Bot

A Telegram bot built with Aiogram 3.x and PyTgCalls 2.1.0 that streams radio stations to voice chats.

## Features

- 🎵 Stream multiple radio stations
- 🎛️ Start/Stop buttons with inline keyboard
- 🔊 High-quality audio with AudioQuality.STUDIO
- 🔄 Auto-reconnect on stream drops
- 🪟 Windows compatibility
- 📱 Telegram bot interface

## Requirements

- Python 3.8+
- FFmpeg installed and in PATH
- Telegram Bot Token
- Telegram API ID and Hash

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - Windows: Download from https://ffmpeg.org/download.html
   - Add FFmpeg to your system PATH

4. Configure the bot:
   - Get your Telegram Bot Token from [@BotFather](https://t.me/BotFather)
   - Get your API ID and Hash from [my.telegram.org](https://my.telegram.org/apps)
   - Edit `config.py` with your credentials
   - Update the radio stream file paths in `config.py`

## Configuration

Edit `config.py` with your settings:

```python
API_TOKEN = "your_bot_token_here"
API_ID = 12345678
API_HASH = "your_api_hash_here"

RADIO_STREAMS = {
    "radio1": {
        "name": "Radio Station 1",
        "path": "C:/absolute/path/to/radio1.mp3"
    },
    "radio2": {
        "name": "Radio Station 2", 
        "path": "C:/absolute/path/to/radio2.mp3"
    }
}
```

## Usage

1. Start the bot:
   ```bash
   python main.py
   ```

2. In Telegram:
   - Send `/start` to see the radio menu
   - Use the inline buttons to start/stop radio streams
   - Use `/stop` to stop the current stream
   - Use `/radio` to show the radio menu again

## Commands

- `/start` - Show welcome message and radio menu
- `/stop` - Stop current radio stream
- `/radio` - Show radio station selection menu

## File Structure

- `main.py` - Main bot implementation
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Notes

- Ensure all audio file paths are absolute paths
- The bot uses PyTgCalls with AudioQuality.STUDIO for high-quality audio
- Windows compatibility is handled with `asyncio.WindowsSelectorEventLoopPolicy()`
- Auto-reconnect attempts 3 times with exponential backoff

## Troubleshooting

1. **FFmpeg not found**: Install FFmpeg and add to PATH
2. **File not found**: Use absolute paths in config
3. **API errors**: Check your API ID, Hash, and Bot Token
4. **Stream drops**: Auto-reconnect will attempt to restore connection

## License

MIT License