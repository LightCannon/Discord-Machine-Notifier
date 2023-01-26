  # Discord Machine Notifier


## Perquisites
 1. Python 3.7+ is required to run this bot.
 2. Your bot added to your server (on which you are receiving the messages). Refer to [here](https://github.com/LightCannon/Discord-Machine-Notifier#creating-a-discord-bot) to create a discord bot.
 3. An email to receive notifications from.

## Installing required modules
Run: pip install -r requirements.txt

## Running the bot
1- Add the configurations in the .env file. Here are the list of configurations and their function:

* **BOT_TOKEN**: Your Discord bot bot token.
* **BOT_CHANNEL_ID**: Discord channel ID which the bot will monitor.
* **MACHINE_TIMEOUT**: Time (in seconds) before which the bot will consider the machine not working if no updates from it got received on the channel.
* **UPDATE_RATE**: Time (in seconds) of periodic updates check (1 means the bot checks for updates every 1 second).
* **RISK_MARGIN_NOTIFICATION_SECONDS**: Time (in seconds) which u will not get any more risk of marging notifications after the first one received.
* **EMAIL_SENDER**: Notification sending email.
* **EMAIL_PASSWORD**: Notification Email password (or application password in case of Gmail, refer to [here](https://support.google.com/accounts/answer/185833?hl=en) to create a one).
* **EMAIL_RECEIVER**: Receiver email to get notifications on.
* **EMAIL_HOST**: smtp host to send emails through (smtp.gmail.com for Gmail).
* **EMAIL_PORT**: smtp port (587).

2- From cmd (or terminal), run: **python main.py**

## Creating a Discord bot

 1.  Go to the Discord Developer Portal ([https://discord.com/developers/applications](https://discord.com/developers/applications)) and sign in.
 2. Click on the "New Application" button to create a new bot.![enter image description here](https://static1.xdaimages.com/wordpress/wp-content/uploads/2022/06/discord-bot-apps-page-1024x550.jpg?q=50&fit=crop&w=943&dpr=1.5)
 3. Give your bot a name and click on the "Create" button.![enter image description here](https://static1.xdaimages.com/wordpress/wp-content/uploads/2022/06/name-your-discord-bot-page-1024x550.jpg?q=50&fit=crop&w=943&dpr=1.5)
 4. It'll now take you to a page in which you can enter details such as your app's description, add tags, an app icon, and more. Once done, hit the _Save Changes_ button to proceed
 5.  Click on the "Bot" section on the left sidebar and then click on "Add Bot."![enter image description here](https://static1.xdaimages.com/wordpress/wp-content/uploads/2022/06/Add-bot-to-your-server-page-1024x436.jpg?q=50&fit=crop&w=943&dpr=1.5)
 6. -   You'll now see a security token for your bot on the next page. If the token hasn't been generated, simply tap on the  _Reset_  button to create a new token. Copy this token ID as we'll need it
 7. Navigate to intents section and enable all of them![enter image description here](https://i.imgur.com/PYFLgAy.png)
 8. Now, look for the OAuth2 option in the menu on the left sidebar and click on it to find your **CLIENT ID**. It's a long string of numbers. ![enter image description here](https://i.imgur.com/JjlbS6H.png)
 9. Paste to this URL below -- replace the word **CLIENTID** with the actual **CLIENT ID** that you just copied -`https://discordapp.com/oauth2/authorize?&client_id=CLIENTID&scope=bot&permissions=8`
 10. Simply paste this particular URL into your web browser and hit enter. It'll open a page in which you can tell Discord where to send your bot. Select the server to which you want to add your new bot from the dropdown menu
