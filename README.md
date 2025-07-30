# Food Wastage Prediction and Redistribution System

A comprehensive web application built with Python Flask that helps reduce food wastage by predicting nearby areas where excess food from events can be redistributed. The system connects event organizers with communities in need, facilitating efficient food redistribution.

## 🌟 Features

### Core Functionality
- **User Registration & Authentication**: Secure user accounts with email and mobile verification
- **Event Management**: Create and manage events with food wastage details
- **Intelligent Prediction**: AI-powered location prediction for optimal food redistribution
- **Real-time Tracking**: Monitor redistribution status and progress
- **Analytics Dashboard**: Comprehensive insights into food wastage reduction impact

### Key Components
- **Event Creation**: Users input event type, location, and food quantity (plates/items)
- **Location Prediction**: System predicts nearby areas where food is needed
- **Redistribution Confirmation**: Users select redistribution locations
- **Team Coordination**: Automated pickup and delivery coordination
- **Impact Analytics**: Track environmental and social impact metrics

## 🚀 Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (with SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Geolocation**: Geopy for location services
- **Authentication**: Flask-Login for user management

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd food-wastage-prediction-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python app.py
```
The database will be automatically created with sample redistribution locations.

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📱 Usage Guide

### For Users

1. **Registration**: Create an account with email, mobile, and password
2. **Login**: Access your personalized dashboard
3. **Create Event**: Input event details and food wastage information
4. **Predict Locations**: View AI-suggested redistribution locations
5. **Confirm Redistribution**: Select a location and confirm pickup
6. **Track Progress**: Monitor the redistribution process
7. **View Analytics**: See your impact on food wastage reduction

### Event Types Supported
- Weddings
- Corporate Events
- Birthday Parties
- Conferences
- Restaurants
- Catering Services
- Festivals
- Other Events

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `mobile`: Mobile number
- `password_hash`: Encrypted password
- `name`: Full name
- `created_at`: Registration timestamp

### Events Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `event_type`: Type of event
- `food_quantity_plates`: Number of plates
- `food_quantity_items`: Number of items
- `location`: Event location
- `latitude/longitude`: GPS coordinates
- `status`: Event status (pending/confirmed)
- `redistribution_location`: Selected redistribution location
- `created_at`: Event creation timestamp

### Redistribution Locations Table
- `id`: Primary key
- `name`: Location name
- `address`: Full address
- `latitude/longitude`: GPS coordinates
- `capacity`: Maximum capacity
- `current_need`: Current food need
- `type`: Location type (shelter, food_bank, etc.)

## 📊 Analytics Features

- **Event Statistics**: Total events, confirmed redistributions
- **Food Impact**: Plates and items saved
- **Environmental Impact**: CO2 emissions prevented, water saved
- **Success Rate**: Redistribution success percentage
- **Visual Charts**: Event types distribution, monthly trends

## 🌍 Environmental Impact

The system calculates environmental benefits:
- **CO2 Emissions Prevented**: Based on food waste reduction
- **Water Saved**: Water used in food production
- **Meals Provided**: People fed through redistribution

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Option 1: Heroku
1. Create a `Procfile`:
```
web: gunicorn app:app
```

2. Add gunicorn to requirements.txt:
```
gunicorn==20.1.0
```

3. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

#### Option 2: Python Anywhere
1. Upload files to PythonAnywhere
2. Set up virtual environment
3. Install requirements
4. Configure WSGI file
5. Set up database

#### Option 3: VPS/Cloud Server
1. Set up server with Python
2. Install dependencies
3. Use Gunicorn + Nginx
4. Set up SSL certificate
5. Configure domain

### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
FLASK_ENV=production
```

## 🔧 Configuration

### Database Configuration
- Default: SQLite (development)
- Production: PostgreSQL/MySQL recommended

### Security Settings
- Change default secret key
- Enable HTTPS in production
- Set up proper authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Bootstrap team for the responsive UI components
- Chart.js for data visualization
- All contributors and users

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact: [your-email@example.com]
- Documentation: [link-to-docs]

## 🔮 Future Enhancements

- Mobile app development
- Real-time notifications
- Advanced ML algorithms
- Integration with food delivery platforms
- Multi-language support
- Advanced analytics and reporting

---

**Made with ❤️ for a sustainable future** 