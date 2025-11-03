#!/bin/bash

# Smart Journalist Deployment Script

set -e  # Exit on any error

echo "🚀 Deploying Smart and Wise Journalist App..."

# Configuration
APP_NAME="smart-journalist"
DEPLOY_ENV="${1:-production}"
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"

echo "📝 Deployment environment: $DEPLOY_ENV"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup current deployment (if exists)
if [ -d "/opt/$APP_NAME" ]; then
    echo "💾 Creating backup of current deployment..."
    cp -r /opt/$APP_NAME/* "$BACKUP_DIR/"
fi

# Create application directory
sudo mkdir -p /opt/$APP_NAME
sudo chown $USER:$USER /opt/$APP_NAME

# Copy application files
echo "📦 Copying application files..."
rsync -av --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' \
    --exclude='.git' --exclude='logs' --exclude='output' \
    ./ /opt/$APP_NAME/

# Set up Python virtual environment
echo "🐍 Setting up Python environment..."
cd /opt/$APP_NAME
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs output

# Set up environment file
if [ ! -f "/opt/$APP_NAME/.env" ]; then
    echo "⚠️  Environment file not found. Creating template..."
    cp .env.example .env
    echo "❗ Please configure /opt/$APP_NAME/.env with your API keys"
fi

# Set up systemd service (optional)
if command -v systemctl &> /dev/null; then
    echo "🔧 Setting up systemd service..."

    sudo tee /etc/systemd/system/smart-journalist.service > /dev/null <<EOF
[Unit]
Description=Smart and Wise Journalist App
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/$APP_NAME
Environment=PATH=/opt/$APP_NAME/venv/bin
ExecStart=/opt/$APP_NAME/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable smart-journalist

    echo "✅ Systemd service created. Start with: sudo systemctl start smart-journalist"
fi

# Set up log rotation
echo "📋 Setting up log rotation..."
sudo tee /etc/logrotate.d/smart-journalist > /dev/null <<EOF
/opt/$APP_NAME/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 $USER $USER
}
EOF

# Set up cron job for daily execution
echo "⏰ Setting up daily cron job..."
(crontab -l 2>/dev/null; echo "0 8 * * * cd /opt/$APP_NAME && ./venv/bin/python main.py >> logs/cron.log 2>&1") | crontab -

# Set permissions
chmod +x /opt/$APP_NAME/scripts/*.sh

echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Post-deployment checklist:"
echo "   1. Configure /opt/$APP_NAME/.env with your API keys"
echo "   2. Test the application: cd /opt/$APP_NAME && python main.py"
echo "   3. Check logs: tail -f /opt/$APP_NAME/logs/smart_journalist.log"
echo "   4. Start systemd service: sudo systemctl start smart-journalist"
echo "   5. Monitor cron execution: tail -f /opt/$APP_NAME/logs/cron.log"
echo ""
echo "🎯 Application deployed to: /opt/$APP_NAME"
echo "📊 Logs location: /opt/$APP_NAME/logs/"
echo "📄 Reports output: /opt/$APP_NAME/output/"
