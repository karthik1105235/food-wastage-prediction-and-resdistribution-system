from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_wastage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Event', backref='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    food_quantity_plates = db.Column(db.Integer, nullable=False)
    food_quantity_items = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    redistribution_location = db.Column(db.String(200))
    redistribution_lat = db.Column(db.Float)
    redistribution_lng = db.Column(db.Float)

class RedistributionLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, default=100)
    current_need = db.Column(db.Integer, default=0)
    type = db.Column(db.String(100), default='shelter')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Sample redistribution locations data
SAMPLE_LOCATIONS = [
    {
        'name': 'Community Food Bank',
        'address': '123 Main Street, Downtown',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'capacity': 200,
        'current_need': 50,
        'type': 'food_bank'
    },
    {
        'name': 'Homeless Shelter',
        'address': '456 Oak Avenue, Midtown',
        'latitude': 40.7589,
        'longitude': -73.9851,
        'capacity': 150,
        'current_need': 75,
        'type': 'shelter'
    },
    {
        'name': 'Senior Center',
        'address': '789 Pine Street, Uptown',
        'latitude': 40.7505,
        'longitude': -73.9934,
        'capacity': 100,
        'current_need': 30,
        'type': 'senior_center'
    },
    {
        'name': 'Youth Center',
        'address': '321 Elm Street, Westside',
        'latitude': 40.7648,
        'longitude': -73.9808,
        'capacity': 120,
        'current_need': 60,
        'type': 'youth_center'
    }
]

def initialize_database():
    with app.app_context():
        db.create_all()
        
        # Add sample redistribution locations if they don't exist
        if RedistributionLocation.query.count() == 0:
            for location_data in SAMPLE_LOCATIONS:
                location = RedistributionLocation(**location_data)
                db.session.add(location)
            db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        name = request.form['name']
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        user = User(
            email=email,
            mobile=mobile,
            password_hash=generate_password_hash(password),
            name=name
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_events = Event.query.filter_by(user_id=current_user.id).order_by(Event.created_at.desc()).all()
    return render_template('dashboard.html', events=user_events)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        event_type = request.form['event_type']
        food_quantity_plates = int(request.form['food_quantity_plates'])
        food_quantity_items = int(request.form['food_quantity_items'])
        location = request.form['location']
        
        # Get coordinates for the location
        geolocator = Nominatim(user_agent="food_wastage_app")
        try:
            location_data = geolocator.geocode(location)
            latitude = location_data.latitude if location_data else None
            longitude = location_data.longitude if location_data else None
        except:
            latitude = None
            longitude = None
        
        event = Event(
            user_id=current_user.id,
            event_type=event_type,
            food_quantity_plates=food_quantity_plates,
            food_quantity_items=food_quantity_items,
            location=location,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('predict_redistribution', event_id=event.id))
    
    return render_template('create_event.html')

@app.route('/predict_redistribution/<int:event_id>')
@login_required
def predict_redistribution(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        flash('Access denied!', 'error')
        return redirect(url_for('dashboard'))
    
    # Get nearby redistribution locations
    redistribution_locations = RedistributionLocation.query.all()
    
    # Calculate distances and sort by proximity
    if event.latitude and event.longitude:
        event_coords = (event.latitude, event.longitude)
        for location in redistribution_locations:
            location_coords = (location.latitude, location.longitude)
            location.distance = geodesic(event_coords, location_coords).kilometers
        redistribution_locations.sort(key=lambda x: x.distance)
    
    return render_template('predict_redistribution.html', 
                         event=event, 
                         locations=redistribution_locations)

@app.route('/confirm_redistribution/<int:event_id>/<int:location_id>')
@login_required
def confirm_redistribution(event_id, location_id):
    event = Event.query.get_or_404(event_id)
    location = RedistributionLocation.query.get_or_404(location_id)
    
    if event.user_id != current_user.id:
        flash('Access denied!', 'error')
        return redirect(url_for('dashboard'))
    
    # Update event with redistribution details
    event.status = 'confirmed'
    event.redistribution_location = location.name
    event.redistribution_lat = location.latitude
    event.redistribution_lng = location.longitude
    
    # Update location's current need
    location.current_need += event.food_quantity_plates
    
    db.session.commit()
    
    flash('Redistribution confirmed! Our team will contact you shortly.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/analytics')
@login_required
def analytics():
    # Get statistics
    total_events = Event.query.count()
    confirmed_events = Event.query.filter_by(status='confirmed').count()
    total_food_plates = db.session.query(db.func.sum(Event.food_quantity_plates)).scalar() or 0
    total_food_items = db.session.query(db.func.sum(Event.food_quantity_items)).scalar() or 0
    
    # Get event types distribution
    event_types = db.session.query(Event.event_type, db.func.count(Event.id)).group_by(Event.event_type).all()
    
    # Get monthly data for charts
    monthly_data = db.session.query(
        db.func.strftime('%Y-%m', Event.created_at),
        db.func.count(Event.id),
        db.func.sum(Event.food_quantity_plates)
    ).group_by(db.func.strftime('%Y-%m', Event.created_at)).all()
    
    return render_template('analytics.html',
                         total_events=total_events,
                         confirmed_events=confirmed_events,
                         total_food_plates=total_food_plates,
                         total_food_items=total_food_items,
                         event_types=event_types,
                         monthly_data=monthly_data)

@app.route('/api/locations')
def api_locations():
    locations = RedistributionLocation.query.all()
    return jsonify([{
        'id': loc.id,
        'name': loc.name,
        'address': loc.address,
        'latitude': loc.latitude,
        'longitude': loc.longitude,
        'capacity': loc.capacity,
        'current_need': loc.current_need,
        'type': loc.type
    } for loc in locations])

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True) 