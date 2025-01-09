Posts images or videos to discord with optional text messages.

![image](https://github.com/user-attachments/assets/57d16eaf-dfe3-4a9c-b502-c1f7c8904789)

![image](https://github.com/user-attachments/assets/80da3779-f01f-4eb9-a702-6d5ead03a23b)


Clone this into our custom_nodes:
     cd ComfyUI_windows_portable\ComfyUI\custom_nodes
     git clone https://github.com/r3dial/redial-discomphy.git

Install requirements (discord..  For Stand-alone embedded python it looks like this from a command line in the comfyui_windows_portable directory:
     cd ComfyUI_windows_portable\
     .\python_embeded\python.exe -m pip install -r .\ComfyUI\custom_nodes\redial-discomphy\requirements.txt
     
Add your Discord Token, Guild, and Channel information to the default.env and rename it to .env

1. Get Discord Token from https://discord.com/developers/applications
     - Create a new Bot, name it.
     - Selec the Bot menu from the left navigation bar
     - Press the Reset Token button to get new token.
3. To get your "Guild ID" and Channel ID: In discord, go into your user Settings, Advanced section, turn on 'Developer Mode'.
4. Now when you right click on your Server name or a channel, you will see a 'Copy Server ID' or 'Copy Channel ID' respectively.
5. Populate the default.env with these values and rename it to .env

