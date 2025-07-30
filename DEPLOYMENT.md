# Deployment Guide - Food Wastage Prediction System

This guide provides step-by-step instructions for deploying the Food Wastage Prediction System to various platforms.

## 🚀 Quick Start

### 1. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:5000
```

### 2. Run Deployment Script
```bash
python deploy.py
```

## 🌐 Production Deployment Options

### Option 1: Heroku Deployment

#### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

#### Steps
1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

### Option 2: PythonAnywhere

#### Steps
1. **Create PythonAnywhere Account**
   - Sign up at www.pythonanywhere.com

2. **Upload Files**
   - Use Files tab to upload your project files
   - Or use Git: `git clone your-repository-url`

3. **Set Up Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 food-wastage-env
   pip install -r requirements.txt
   ```

4. **Configure WSGI File**
   - Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Add your application path

5. **Set Up Database**
   - Use PythonAnywhere's MySQL or SQLite

6. **Reload Web App**
   - Click "Reload" in Web tab

### Option 3: VPS/Cloud Server (Ubuntu)

#### Prerequisites
- Ubuntu server with Python 3.8+
- Nginx
- Supervisor

#### Steps
1. **Server Setup**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx supervisor
   ```

2. **Clone Repository**
   ```bash
   git clone your-repository-url
   cd food-wastage-prediction-system
   ```

3. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Gunicorn**
   ```bash
   # Create gunicorn config
   sudo nano /etc/supervisor/conf.d/food-wastage.conf
   ```

   Add:
   ```ini
   [program:food-wastage]
   directory=/path/to/your/app
   command=/path/to/your/app/venv/bin/gunicorn app:app -w 4 -b 127.0.0.1:8000
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/food-wastage.err.log
   stdout_logfile=/var/log/food-wastage.out.log
   user=www-data
   ```

5. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/food-wastage
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/food-wastage /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl reload nginx
   ```

7. **Start Services**
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start food-wastage
   ```

### Option 4: Railway

#### Steps
1. **Connect GitHub Repository**
   - Go to railway.app
   - Connect your GitHub account
   - Select your repository

2. **Configure Environment**
   - Set environment variables in Railway dashboard
   - Add `SECRET_KEY` and `FLASK_ENV=production`

3. **Deploy**
   - Railway will automatically deploy on push
   - Get your live URL from dashboard

## 🔧 Environment Configuration

### Required Environment Variables
```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_URL=your-database-url
```

### Database Configuration

#### SQLite (Development)
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///food_wastage.db'
```

#### PostgreSQL (Production)
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@host:port/database'
```

#### MySQL (Production)
```python
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@host:port/database'
```

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Change default secret key
- [ ] Enable HTTPS/SSL
- [ ] Set up proper firewall rules
- [ ] Use environment variables for sensitive data
- [ ] Regular security updates
- [ ] Database backup strategy
- [ ] Monitor application logs

### SSL Certificate Setup

#### Let's Encrypt (Free)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### Manual SSL Setup
1. Purchase SSL certificate
2. Upload certificate files
3. Configure Nginx/Apache
4. Redirect HTTP to HTTPS

## 📊 Monitoring & Maintenance

### Application Monitoring
- Set up logging
- Monitor error rates
- Track performance metrics
- Set up alerts

### Database Maintenance
- Regular backups
- Monitor database size
- Optimize queries
- Clean up old data

### Updates & Maintenance
- Keep dependencies updated
- Monitor security advisories
- Regular application updates
- Performance optimization

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

#### 2. Database Connection Issues
```bash
# Check database URL
# Ensure database server is running
# Verify credentials
```

#### 3. Port Already in Use
```bash
# Find process using port
lsof -i :5000
# Kill process or change port
```

#### 4. Permission Issues
```bash
# Fix file permissions
chmod +x app.py
chmod 755 templates/
```

#### 5. Static Files Not Loading
```bash
# Check file paths
# Verify static folder configuration
# Clear browser cache
```

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test locally first
4. Check platform-specific documentation
5. Create issue in repository

## 🔄 Continuous Deployment

### GitHub Actions Setup
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

---

**Happy Deploying! 🚀** 