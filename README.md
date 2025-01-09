# Redial Discomphy - Discord Integration for ComfyUI

A custom node for ComfyUI that enables direct posting of images, videos, and messages to Discord channels. This node seamlessly integrates your ComfyUI workflows with Discord communication, allowing you to automatically share your generated content.

## Features

- Post images directly from ComfyUI workflows to Discord
- Support for both generated images and existing media files
- Custom message support with each post
- Automatic retry mechanism for reliable message delivery
- Real-time status feedback
- Multi-file support in a single message

## Prerequisites

- ComfyUI installed
- Discord account
- Discord bot token with proper permissions
- Discord server (guild) with a designated channel

## Installation

### For ComfyUI Windows Portable:

1. Navigate to your ComfyUI custom nodes directory:
```bash
cd ComfyUI_windows_portable\ComfyUI\custom_nodes
```

2. Clone this repository:
```bash
git clone https://github.com/r3dial/redial-discomphy.git
```

3. Install requirements:
```bash
cd ComfyUI_windows_portable
.\python_embeded\python.exe -m pip install -r .\ComfyUI\custom_nodes\redial-discomphy\requirements.txt
```

### For Standard ComfyUI Installation:

1. Navigate to your ComfyUI custom nodes directory and clone the repository
2. Install requirements using pip:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a Discord Bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Navigate to the "Bot" section
   - Click "Reset Token" to get your bot token
   - Enable necessary bot permissions (Send Messages, Attach Files)
   - Use the OAuth2 URL Generator to invite the bot to your server

2. Enable Developer Mode in Discord:
   - Open Discord Settings
   - Go to "App Settings" → "Advanced"
   - Enable "Developer Mode"

3. Get Required IDs:
   - Right-click your server name → "Copy Server ID" (This is your Guild ID)
   - Right-click the target channel → "Copy Channel ID"

4. Set Up Environment File:
   - Copy `default.env` to `.env`
   - Fill in your details:
     ```env
     DISCORD_TOKEN=your_bot_token_here
     GUILD=your_guild_id_here
     CHANNEL=your_channel_id_here
     ```

## Usage

The Discord Message node provides several input options:

- **Image**: Connect to any node that outputs an image
- **Message Input**: Primary message text
- **Media Path**: Optional path to an external image/video file
- **Message**: Additional message text (appended to Message Input)

### Example Workflows

1. **Basic Image Posting**:
   - Connect your image generation node to the Discord Message node
   - Add a message in the "Message Input" field
   - Execute the workflow to post the generated image with your message

2. **External Media Posting**:
   - Leave the image input disconnected
   - Provide the path to your media file in "Media Path"
   - Add your message
   - Execute to post the external media

## Troubleshooting

### Common Issues

1. **"Discord client not initialized"**
   - Check if your `.env` file is properly configured
   - Verify your bot token is valid
   - Restart ComfyUI

2. **"Discord client not ready"**
   - Wait a few seconds and try again
   - Check your internet connection
   - Verify the bot is properly invited to your server

3. **"Media file not found"**
   - Verify the file path is correct
   - Check if the file exists
   - Ensure proper file permissions

### Tips

- The node includes an automatic retry mechanism for failed messages
- Check the node's output for detailed status messages
- Keep your bot token secure and never share it publicly
- Ensure your bot has proper permissions in the Discord channel

## License

See the [LICENSE](LICENSE) file for details.
