from telethon import TelegramClient, events
import requests
import os

# Load credentials from environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Validate that all required environment variables are set
if not all([api_id, api_hash, phone, bot_token]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

# Use session file in /app/sessions directory for Docker volume mounting
session_path = os.getenv('SESSION_PATH', '/app/sessions/session_name')
client = TelegramClient(session_path, api_id, api_hash)

async def get_file_url(file_id):
    url = f"https://api.telegram.org/bot{bot_token}/getFile"
    params = {'file_id': file_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        file_path = response.json()['result']['file_path']
        file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        return file_url
    return None

# Event handler for new messages
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if event.is_channel:
        channel = await event.get_chat()
        message = event.message
        
        # Filter channels by title or username
        channel_info = [
            {'username': 'beritairan', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'almanarnews', 'country_code': 'LB', 'country_name': 'Lebanon'},
            {'username': 'TheSimurgh313', 'country_code': 'IR', 'country_name': 'Iran'},
            {'username': 'geopolitics_live', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'ukr_leaks_eng', 'country_code': 'UA', 'country_name': 'Ukraine'},
            {'username': 'arrahmahnews', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'LebUpdate', 'country_code': 'LB', 'country_name': 'Lebanon'},
            {'username': 'Middle_East_Spectator', 'country_code': 'MDE', 'country_name': 'Middle East'},
            {'username': 'PalestinaPost', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'thecradlemedia', 'country_code': 'MDE', 'country_name': 'Middle East'},            
            {'username': 'ukraine_watch', 'country_code': 'UA', 'country_name': 'Ukraine'},
            {'username': 'enemywatch', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'TheTimesOfIsrael2022', 'country_code': 'IL', 'country_name': 'Israel'},
            {'username': 'almayadeenenglish', 'country_code': 'SA', 'country_name': 'Saudi Arabia'},
            {'username': 'QudsNen', 'country_code': 'PS', 'country_name': 'Palestine'},
            {'username': 'presstv', 'country_code': 'IR', 'country_name': 'Iran'},
            {'username': 'KurdishFrontNews', 'country_code': 'KRG', 'country_name': 'Kurdistan'},
            {'username': 'R_Diplomat', 'country_code': 'RU', 'country_name': 'Russian Federation'},
            {'username': 'Journalyze', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'tafsirhikmah', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'informante_universal', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'TheIslanderNews', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'gazaalanpa', 'country_code': 'PS', 'country_name': 'Palestine'},
            {'username': 'gazaalannet', 'country_code': 'PS', 'country_name': 'Palestine'},
            {'username': 'ibnuali14', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'porosperlawanan', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'bricsnews', 'country_code': 'XX', 'country_name': 'BRICS'},
            {'username': 'two_majors', 'country_code': 'XX', 'country_name': 'BRICS'},
            {'username': 'PalestineResist', 'country_code': 'PS', 'country_name': 'Palestine'},
            {'username': 'Slavyangrad', 'country_code': 'UA', 'country_name': 'Ukraine'},
            {'username': 'myLordBebo', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'SputnikInt', 'country_code': 'RU', 'country_name': 'Russian Federation'},
            {'username': 'mayadeenchannel', 'country_code': 'SA', 'country_name': 'Saudi Arabia'},
            {'username': 'MiddleEastEye_TG', 'country_code': 'MDE', 'country_name': 'Middle East'},
            {'username': 'DDGeopolitics', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'warmonitors', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'FreePalestineNetwork', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'aljazeeraglobal', 'country_code': 'QA', 'country_name': 'Qatar'},
            {'username': 'The_Jerusalem_Post', 'country_code': 'IL', 'country_name': 'Israel'},
            {'username': 'European_dissident', 'country_code': 'EU', 'country_name': 'European Union'},
            {'username': 'InfoDefenseENGLISH', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'sputnik_afrique', 'country_code': 'RU', 'country_name': 'Russian Federation'},
            {'username': 'megatron_ron', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'yourantifakenews', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'Irna_en', 'country_code': 'IR', 'country_name': 'Iran'},
            {'username': 'medmannews', 'country_code': 'MDE', 'country_name': 'Middle East'},
            {'username': 'RiseGS', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'sputnik_africa', 'country_code': 'RU', 'country_name': 'Russian'},
            {'username': 'IsnewsIndonesia', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'IRIran_Military', 'country_code': 'IR', 'country_name': 'Iran'},
            {'username': 'Sabililungan', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'geo_gaganauts', 'country_code': 'INT', 'country_name': 'International'},
            {'username': 'PhantomSchewiz', 'country_code': 'DE', 'country_name': 'Germany'},
            {'username': 'saharanewschannel', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'Maulatv', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'ConflictChronicles', 'country_code': 'UA', 'country_name': 'Ukraine'},
            {'username': 'islamtsaqolain', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'the_american_majority', 'country_code': 'US', 'country_name': 'United States of America'},
            {'username': 'PeperanganLunakMedia', 'country_code': 'ID', 'country_name': 'Indonesia'},
            {'username': 'MiddleEastMonitor1', 'country_code': 'MDE', 'country_name': 'Middle East'},
            {'username': 'militaernews', 'country_code': 'DE', 'country_name': 'Germany'},
        ]
        
        # Extract just usernames for checking
        allowed_usernames = [channel['username'] for channel in channel_info]
        
        if (getattr(channel, 'username', '') in allowed_usernames):
            # Get country info for this channel
            channel_username = getattr(channel, 'username', '')
            channel_country_info = next(
                (item for item in channel_info if item['username'] == channel_username),
                {'country_code': 'N/A', 'country_name': 'Unknown'}
            )
            
            print(f"Channel Country: {channel_country_info['country_name']}")
            print(f"Channel Country Code: {channel_country_info['country_code']}")
            
            # Print channel details
            print("\n=== Channel Details ===")
            print(f"Channel ID: {channel.id}")
            print(f"Channel Title: {channel.title}")
            print(f"Channel Username: {getattr(channel, 'username', 'No username')}")
            
            # Get channel URL
            if getattr(channel, 'username', None):
                channel_url = f"https://t.me/{channel.username}"
            else:
                # For private channels that use invite links
                try:
                    channel_url = f"https://t.me/c/{channel.id}"
                except:
                    channel_url = "No public URL available"
            
            print(f"Channel URL: {channel_url}")
            print(f"Channel Participants: {getattr(channel, 'participants_count', 'N/A')}")
            
            # Print message details
            print("\n=== Message Details ===")
            print(f"Message ID: {message.id}")
            print(f"Message Date: {message.date}")
            # Format the date to match required format
            formatted_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Clean and format the title and content
            if message.text:
                # Get first 10 words for title
                title = ' '.join(message.text.split()[:10])
                title = title.strip()
                if len(title) >= 100:
                    title = title[:97] + "..."
                
                # Use full text for content
                content = message.text.strip()
            else:
                title = "No title available"
                content = "No content available"

            print(f"Message Title: {title}")
            print(f"Message Text: {content}")
            print(f"Has Media: {message.media is not None}")
            """
            if message.media:
                try:
                    if hasattr(message.media, 'photo'):
                        print("Media Type: Photo")
                        # Download photo
                        path = await client.download_media(
                            message.media,
                            "downloads/photos/"  # Make sure this directory exists
                        )
                        print(f"Photo downloaded to: {path}")
                    
                    elif hasattr(message.media, 'document'):
                        # Check if it's a video by MIME type
                        mime_type = message.media.document.mime_type
                        if mime_type and mime_type.startswith('video/'):
                            print("Media Type: Video")
                            path = await client.download_media(
                                message.media,
                                "downloads/videos/"  # Make sure this directory exists
                            )
                            print(f"Video downloaded to: {path}")
                except Exception as e:
                    print(f"Error downloading media: {str(e)}")
            """
            print(f"Forward Info: {message.forward}")
            print(f"Views: {getattr(message, 'views', 'N/A')}")
            print("=" * 50 + "\n")
            # Here, you'll add code to store the message (Step 6)
            # Send the message to API URL that has been created
            # URL "http://news-api.mediakautsar.com/telegram"
            # Method POST
            # Body Parameter Mapping
            # 'title' => message.title
            # 'content' => message.text
            # 'url' => channel_url
            # 'published_at' => message.date
            # 'country_code' => channel_country_info['country_code']
            # 'country_name' => channel_country_info['country_name']
            # 'source_name' => channel.title
            # Prepare data for API
            payload = {
                "title": title,
                "content": content,
                "url": channel_url,
                "published_at": formatted_date,
                "country_code": channel_country_info['country_code'],
                "country_name": channel_country_info['country_name'],
                "source_name": channel.title
            }

            print(payload)  # For debugging

            # Send to API
            try:
                response = requests.post(
                    'https://news-api.mediakautsar.com/telegram',
                    json=payload,
                    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'}
                )
                
                if response.status_code == 200 or response.status_code == 201:
                    print("Successfully sent to API")
                else:
                    print(f"Failed to send to API. Status code: {response.status_code}")
                    print(f"Response: {response.text}")
            except Exception as e:
                print(f"Error sending to API: {str(e)}")
        
        else:
            # Skip messages from other channels
            return

async def main():
    await client.start(phone)
    print("Client connected! Listening for messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())