import discord
import asyncio
import os
import torch
import numpy as np
from PIL import Image
from dotenv import load_dotenv
import folder_paths
import time

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD'))
CHANNEL_ID = int(os.getenv('CHANNEL'))

class CustomDiscordClient(discord.Client):
    async def setup_hook(self):
        self.message_queue = asyncio.Queue()
        self.bg_task = self.loop.create_task(self.process_message_queue())
        self.ready_event = asyncio.Event()
        self.last_result = "Initializing..."
        
    async def on_ready(self):
        self.ready_event.set()
        self.last_result = "Connected to Discord"
        
    async def process_message_queue(self):
        while True:
            try:
                message_data = await self.message_queue.get()
                channel = self.get_channel(CHANNEL_ID)
                if channel:
                    text = message_data.get('text', '')
                    files = message_data.get('files', [])
                    max_retries = 3
                    retry_delay = 2  # seconds
                    
                    for attempt in range(max_retries):
                        try:
                            discord_files = []
                            for file_path in files:
                                if os.path.exists(file_path):
                                    discord_files.append(discord.File(file_path))
                            
                            if discord_files:
                                await channel.send(content=text if text else None, files=discord_files)
                            else:
                                await channel.send(content=text)
                            
                            self.last_result = f"Message sent successfully (Attempt {attempt + 1})"
                            break
                        except Exception as e:
                            if attempt < max_retries - 1:
                                self.last_result = f"Retry {attempt + 1}/{max_retries}: {str(e)}"
                                await asyncio.sleep(retry_delay)
                            else:
                                self.last_result = f"Failed after {max_retries} attempts: {str(e)}"
                                raise
                        
                self.message_queue.task_done()
            except Exception as e:
                self.last_result = f"Error processing message: {str(e)}"
                print(self.last_result)

class DiscordMessageNode:
    _instance = None
    client = None
    connection_status = "Not Connected"
    retry_count = 0
    max_retries = 3
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.setup_client()
        return cls._instance

    @classmethod
    def setup_client(cls):
        if cls.client is None:
            intents = discord.Intents.default()
            cls.client = CustomDiscordClient(intents=intents)
            
            async def start_client():
                while cls.retry_count < cls.max_retries:
                    try:
                        cls.connection_status = f"Connecting (Attempt {cls.retry_count + 1}/{cls.max_retries})..."
                        await cls.client.start(DISCORD_TOKEN)
                        break
                    except Exception as e:
                        cls.retry_count += 1
                        if cls.retry_count >= cls.max_retries:
                            cls.connection_status = f"Failed to connect: {str(e)}"
                            break
                        print(f"Connection attempt {cls.retry_count} failed, retrying...")
                        await asyncio.sleep(2)  # Wait before retry
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            def run_client():
                loop.run_until_complete(start_client())
            
            import threading
            client_thread = threading.Thread(target=run_client, daemon=True)
            client_thread.start()
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "message_input": ("STRING", {
                    "multiline": True,
                    "placeholder": "Input message"
                }),
                "media_path": ("STRING", {
                    "multiline": False,
                    "placeholder": "Path to image/video file"
                }),
                "message": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Additional message text"
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("discord_result",)
    FUNCTION = "send_message"
    CATEGORY = "messaging"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")  # Always update
    
    def send_message(self, message="", image=None, media_path=None, message_input=None, unique_id=None):
        try:
            # Wait for client to be ready with timeout
            if not self.client:
                return ("Discord client not initialized",)
            
            # Update status widget
            status_text = "Connected" if self.client.is_ready() else self.connection_status
            
            if not self.client.is_ready():
                # Wait for ready with timeout
                print("Waiting for Discord connection...")
                # Wait up to 5 seconds for connection
                for _ in range(10):
                    if self.client.is_ready():
                        print("Connected successfully")
                        break
                    time.sleep(0.5)
                if not self.client.is_ready():
                    return ("Discord client not ready - Please try again",)

            files = []
            result_text = []
            
            # Handle image tensor if provided
            if image is not None:
                # Convert tensor to PIL Image
                i = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8)[0])
                
                # Save to temporary file
                temp_dir = folder_paths.get_temp_directory()
                temp_file = os.path.join(temp_dir, f"discord_temp_{unique_id}.png")
                img.save(temp_file)
                files.append(temp_file)
                result_text.append("Added image from tensor")
            
            # Handle media path if provided
            if media_path:
                if os.path.exists(media_path):
                    files.append(media_path)
                    result_text.append(f"Added media file: {os.path.basename(media_path)}")
                else:
                    result_text.append(f"Warning: Media file not found: {media_path}")
            
            # Combine message_input with message text
            # If message_input is provided, add message text after it
            # If message_input is empty/None, just use message text
            final_message = ""
            if message_input:
                final_message = message_input
                result_text.append("Using input message")
            if message:
                if final_message:
                    final_message += "\n" + message
                    result_text.append("Added additional message text")
                else:
                    final_message = message
                    result_text.append("Using message text")
            
            # If no message but we have files, use filename as message
            if not final_message and files:
                final_message = os.path.basename(files[0])
                result_text.append("Using filename as message")
            
            message_data = {
                'text': final_message,
                'files': files
            }
            
            asyncio.run_coroutine_threadsafe(
                self.client.message_queue.put(message_data),
                self.client.loop
            )
            
            # Wait a bit for the message to be processed
            time.sleep(0.5)
            
            # Return the Discord result
            return (self.client.last_result,)
            
        except Exception as e:
            error_msg = str(e)
            return (f"Error: {error_msg}",)

# Register the node
NODE_CLASS_MAPPINGS = {
    "DiscordMessage": DiscordMessageNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DiscordMessage": "Discord Message"
}
