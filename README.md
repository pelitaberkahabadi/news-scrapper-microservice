# News Scraper Microservice

A Telegram bot microservice that monitors news channels and forwards content to an API endpoint.

## Features

- 📰 Monitors 60+ Telegram news channels from around the world
- 🔄 Real-time message scraping and forwarding
- 🌍 Multi-region coverage (Middle East, Asia, Europe, Americas)
- 🐳 Fully containerized with Docker
- 🔐 Secure credential management via environment variables
- 💾 Persistent session management

## Prerequisites

- Docker and Docker Compose installed
- Telegram API credentials (get from [https://my.telegram.org/apps](https://my.telegram.org/apps))
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- Active Telegram account with access to the channels you want to monitor

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd news-scrapper-microservice
```

### 2. Set Up Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone_number
TELEGRAM_BOT_TOKEN=your_bot_token
```

### 3. Create Sessions Directory

```bash
mkdir -p sessions
```

### 4. Build and Run with Docker Compose

```bash
docker-compose up -d
```

The bot will start and begin monitoring configured channels.

## Docker Commands

### Build the Docker Image

```bash
docker-compose build
```

### Start the Service

```bash
# Start in background
docker-compose up -d

# Start with logs visible
docker-compose up
```

### Stop the Service

```bash
docker-compose down
```

### View Logs

```bash
# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

### Restart the Service

```bash
docker-compose restart
```

### Check Service Status

```bash
docker-compose ps
```

### Access Container Shell

```bash
docker-compose exec telegram-news-scraper /bin/bash
```

## Manual Docker Commands (Without Compose)

### Build the Image

```bash
docker build -t news-scraper:latest .
```

### Run the Container

```bash
docker run -d \
  --name news-scraper-bot \
  --env-file .env \
  -v $(pwd)/sessions:/app/sessions \
  --restart unless-stopped \
  news-scraper:latest
```

### Stop and Remove Container

```bash
docker stop news-scraper-bot
docker rm news-scraper-bot
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_API_ID` | Your Telegram API ID | Yes |
| `TELEGRAM_API_HASH` | Your Telegram API Hash | Yes |
| `TELEGRAM_PHONE` | Your phone number with country code | Yes |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Yes |
| `SESSION_PATH` | Path to session file | No (default: `/app/sessions/session_name`) |

### Monitored Channels

The bot monitors 60+ news channels from various regions including:
- 🇮🇩 Indonesia
- 🇮🇷 Iran
- 🇱🇧 Lebanon
- 🇮🇱 Israel
- 🇵🇸 Palestine
- 🇺🇦 Ukraine
- 🇷🇺 Russia
- 🌍 International sources

See [`public/bot.py`](public/bot.py) for the complete list of channels.

### API Endpoint

Scraped news is forwarded to:
- **URL**: `https://news-api.mediakautsar.com/telegram`
- **Method**: POST
- **Content-Type**: application/json

**Payload structure:**
```json
{
  "title": "Article title",
  "content": "Full article content",
  "url": "Channel URL",
  "published_at": "2024-12-03 12:00:00",
  "country_code": "ID",
  "country_name": "Indonesia",
  "source_name": "Channel Name"
}
```

## Session Management

The bot uses Telegram sessions to avoid repeated authentication. Sessions are stored in the `sessions/` directory and mounted as a Docker volume for persistence.

### First Run - Authentication

On first run, the bot will request authentication:

1. View the container logs:
   ```bash
   docker-compose logs -f
   ```

2. You'll see a prompt to enter the verification code sent to your Telegram account

3. The session will be saved and reused for subsequent runs

### Backup Sessions

It's recommended to backup your session files:

```bash
cp -r sessions/ sessions-backup/
```

## Troubleshooting

### Container Keeps Restarting

Check the logs:
```bash
docker-compose logs --tail=50
```

Common issues:
- Missing environment variables
- Invalid credentials
- Session file corruption

### Session Expired

If you see authentication errors:
1. Stop the container: `docker-compose down`
2. Remove old session files: `rm sessions/*`
3. Restart: `docker-compose up -d`
4. Complete authentication again

### Permission Issues

Ensure the sessions directory is writable:
```bash
chmod 755 sessions/
```

### Port Conflicts

The bot doesn't expose any ports by default, but if you need to add health check endpoints or monitoring, update the `docker-compose.yml` accordingly.

## Monitoring

### Health Check

The container includes a health check that monitors the Python process:

```bash
docker inspect --format='{{json .State.Health}}' news-scraper-bot
```

### Resource Usage

Check container resource usage:
```bash
docker stats news-scraper-bot
```

## Development

### Local Development Without Docker

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export TELEGRAM_API_ID=your_api_id
   export TELEGRAM_API_HASH=your_api_hash
   export TELEGRAM_PHONE=your_phone
   export TELEGRAM_BOT_TOKEN=your_token
   export SESSION_PATH=./session_name
   ```

4. Run the bot:
   ```bash
   python public/bot.py
   ```

### Modifying Monitored Channels

Edit the `channel_info` list in [`public/bot.py`](public/bot.py:29-91) to add or remove channels.

## Security Notes

- ⚠️ **Never commit `.env` files** to version control
- 🔒 Keep your API credentials secure
- 💾 Backup session files securely
- 🔄 Rotate credentials periodically
- 🛡️ Use read-only volumes where possible

## Production Deployment

### Using Docker Swarm

```bash
docker stack deploy -c docker-compose.yml news-scraper
```

### Using Kubernetes

Create a ConfigMap for environment variables and a PersistentVolume for sessions.

### Cloud Platforms

The containerized app can be deployed to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue in the repository.
