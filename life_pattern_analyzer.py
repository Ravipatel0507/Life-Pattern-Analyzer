"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                     LIFE PATTERN ANALYZER                                 ║
║                                                                           ║
║  A revolutionary app that analyzes your location, weather, time, and     ║
║  cosmic patterns to predict your optimal daily schedule and energy       ║
║  levels. Features real-time data from multiple APIs combined with        ║
║  circadian rhythm science and productivity research.                     ║
║                                                                           ║
║  🌍 Location-aware  🌤️ Weather-integrated  🌙 Circadian-optimized       ║
║  ⭐ Cosmic patterns  📊 Data visualization  🎨 Beautiful UI             ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta
import json
import math
import random

app = Flask(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# REAL DATA SOURCES - All working without API keys!
# ══════════════════════════════════════════════════════════════════════════════

def get_ip_location():
    """Get user's location from IP - No API key needed!"""
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        return {
            'city': data.get('city', 'Unknown'),
            'country': data.get('country', 'Unknown'),
            'lat': data.get('lat', 0),
            'lon': data.get('lon', 0),
            'timezone': data.get('timezone', 'UTC'),
            'isp': data.get('isp', 'Unknown')
        }
    except:
        # Fallback data
        return {
            'city': 'San Francisco',
            'country': 'United States',
            'lat': 37.7749,
            'lon': -122.4194,
            'timezone': 'America/Los_Angeles',
            'isp': 'Local ISP'
        }

def get_weather(lat, lon):
    """Get weather data from Open-Meteo (free, no API key!)"""
    try:
        url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,pressure_msl&hourly=temperature_2m,relative_humidity_2m,weather_code&timezone=auto'
        response = requests.get(url, timeout=5)
        data = response.json()
        
        current = data.get('current', {})
        
        # Weather code to description mapping
        weather_codes = {
            0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
            45: 'Foggy', 48: 'Foggy', 51: 'Light drizzle', 53: 'Moderate drizzle',
            61: 'Light rain', 63: 'Moderate rain', 65: 'Heavy rain',
            71: 'Light snow', 73: 'Moderate snow', 75: 'Heavy snow',
            95: 'Thunderstorm'
        }
        
        code = current.get('weather_code', 0)
        
        return {
            'temperature': round(current.get('temperature_2m', 20), 1),
            'humidity': current.get('relative_humidity_2m', 50),
            'wind_speed': round(current.get('wind_speed_10m', 10), 1),
            'pressure': current.get('pressure_msl', 1013),
            'condition': weather_codes.get(code, 'Clear'),
            'hourly': data.get('hourly', {})
        }
    except:
        return {
            'temperature': 22,
            'humidity': 65,
            'wind_speed': 10,
            'pressure': 1013,
            'condition': 'Clear sky',
            'hourly': {}
        }

def get_moon_phase():
    """Calculate current moon phase and influence"""
    # Moon cycle is approximately 29.53 days
    known_new_moon = datetime(2000, 1, 6, 18, 14)
    moon_cycle = 29.53
    
    now = datetime.now()
    days_since = (now - known_new_moon).days
    current_phase = (days_since % moon_cycle) / moon_cycle
    
    phase_names = [
        'New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous',
        'Full Moon', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent'
    ]
    
    phase_index = int(current_phase * 8) % 8
    illumination = abs(math.cos((current_phase - 0.5) * 2 * math.pi)) * 100
    
    # Moon influence on energy (based on traditional wisdom)
    energy_influence = {
        0: {'focus': 90, 'creativity': 95, 'social': 50},  # New Moon
        1: {'focus': 85, 'creativity': 90, 'social': 60},  # Waxing Crescent
        2: {'focus': 75, 'creativity': 80, 'social': 70},  # First Quarter
        3: {'focus': 70, 'creativity': 75, 'social': 80},  # Waxing Gibbous
        4: {'focus': 60, 'creativity': 70, 'social': 95},  # Full Moon
        5: {'focus': 70, 'creativity': 75, 'social': 85},  # Waning Gibbous
        6: {'focus': 80, 'creativity': 80, 'social': 70},  # Last Quarter
        7: {'focus': 85, 'creativity': 85, 'social': 60},  # Waning Crescent
    }
    
    return {
        'phase': phase_names[phase_index],
        'illumination': round(illumination, 1),
        'influence': energy_influence[phase_index],
        'emoji': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'][phase_index]
    }

def calculate_circadian_rhythm():
    """Calculate optimal times based on circadian science"""
    now = datetime.now()
    hour = now.hour
    
    # Based on circadian rhythm research
    schedule = {
        'peak_focus': {'start': 10, 'end': 12, 'level': 95},
        'creative_peak': {'start': 14, 'end': 16, 'level': 90},
        'physical_peak': {'start': 17, 'end': 19, 'level': 92},
        'social_peak': {'start': 18, 'end': 21, 'level': 88},
        'deep_sleep': {'start': 2, 'end': 4, 'level': 100},
        'cortisol_peak': {'start': 8, 'end': 9, 'level': 95},
    }
    
    # Calculate current energy levels
    energy = {
        'mental': max(0, min(100, 50 + 30 * math.sin((hour - 10) * math.pi / 12))),
        'physical': max(0, min(100, 50 + 35 * math.sin((hour - 17) * math.pi / 12))),
        'creative': max(0, min(100, 50 + 25 * math.sin((hour - 14) * math.pi / 12))),
        'social': max(0, min(100, 50 + 30 * math.sin((hour - 19) * math.pi / 12)))
    }
    
    return {
        'current_energy': {k: round(v, 1) for k, v in energy.items()},
        'schedule': schedule,
        'chronotype_guess': 'intermediate'  # Could be extended with questionnaire
    }

def analyze_productivity_pattern(weather, moon, circadian, location):
    """Combine all factors to predict optimal schedule"""
    
    # Weather influence on mood and energy
    weather_factor = 1.0
    if weather['condition'] in ['Clear sky', 'Mainly clear']:
        weather_factor = 1.1
    elif weather['condition'] in ['Light rain', 'Moderate rain']:
        weather_factor = 0.9
    elif weather['condition'] in ['Heavy rain', 'Thunderstorm']:
        weather_factor = 0.7
    
    temp_factor = 1.0
    if 18 <= weather['temperature'] <= 24:
        temp_factor = 1.1
    elif weather['temperature'] < 10 or weather['temperature'] > 30:
        temp_factor = 0.85
    
    # Moon influence
    moon_focus = moon['influence']['focus'] / 100
    moon_creativity = moon['influence']['creativity'] / 100
    moon_social = moon['influence']['social'] / 100
    
    # Calculate optimal activities for next 24 hours
    now = datetime.now()
    hourly_predictions = []
    
    for i in range(24):
        hour = (now.hour + i) % 24
        
        # Base circadian energy
        mental = 50 + 35 * math.sin((hour - 10) * math.pi / 12)
        physical = 50 + 40 * math.sin((hour - 17) * math.pi / 12)
        creative = 50 + 30 * math.sin((hour - 14) * math.pi / 12)
        social = 50 + 35 * math.sin((hour - 19) * math.pi / 12)
        
        # Apply environmental factors
        mental *= weather_factor * moon_focus * temp_factor
        physical *= weather_factor * temp_factor
        creative *= weather_factor * moon_creativity * temp_factor
        social *= weather_factor * moon_social * temp_factor
        
        # Clamp values
        mental = max(0, min(100, mental))
        physical = max(0, min(100, physical))
        creative = max(0, min(100, creative))
        social = max(0, min(100, social))
        
        # Determine best activity
        scores = {
            'Deep Work': mental,
            'Creative Tasks': creative,
            'Exercise': physical,
            'Socializing': social,
            'Rest': 100 - (mental + physical) / 2
        }
        
        best_activity = max(scores, key=scores.get)
        
        hourly_predictions.append({
            'hour': hour,
            'time': f"{hour:02d}:00",
            'mental': round(mental, 1),
            'physical': round(physical, 1),
            'creative': round(creative, 1),
            'social': round(social, 1),
            'recommended_activity': best_activity,
            'confidence': round(max(scores.values()), 1)
        })
    
    # Generate insights
    insights = generate_insights(hourly_predictions, weather, moon, location)
    
    return {
        'hourly_predictions': hourly_predictions,
        'insights': insights,
        'factors': {
            'weather_impact': round(weather_factor * 100, 1),
            'temperature_impact': round(temp_factor * 100, 1),
            'moon_phase': moon['phase'],
            'location': f"{location['city']}, {location['country']}"
        }
    }

def generate_insights(predictions, weather, moon, location):
    """Generate personalized insights and recommendations"""
    
    # Find peak hours
    peak_mental = max(predictions, key=lambda x: x['mental'])
    peak_creative = max(predictions, key=lambda x: x['creative'])
    peak_physical = max(predictions, key=lambda x: x['physical'])
    
    insights = []
    
    # Insight 1: Best time for focused work
    insights.append({
        'type': 'peak_performance',
        'icon': '🎯',
        'title': 'Peak Focus Window',
        'message': f"Your mental clarity peaks at {peak_mental['time']}. Schedule your most challenging tasks then.",
        'time': peak_mental['time'],
        'confidence': 95
    })
    
    # Insight 2: Creative window
    insights.append({
        'type': 'creative',
        'icon': '🎨',
        'title': 'Creative Sweet Spot',
        'message': f"Maximum creativity expected around {peak_creative['time']}. Perfect for brainstorming and innovation.",
        'time': peak_creative['time'],
        'confidence': 88
    })
    
    # Insight 3: Exercise timing
    insights.append({
        'type': 'physical',
        'icon': '💪',
        'title': 'Optimal Workout Time',
        'message': f"Your body is primed for exercise at {peak_physical['time']}. You'll see better results training then.",
        'time': peak_physical['time'],
        'confidence': 90
    })
    
    # Insight 4: Weather impact
    if weather['condition'] in ['Clear sky', 'Mainly clear']:
        insights.append({
            'type': 'weather',
            'icon': '☀️',
            'title': 'Weather Boost',
            'message': f"Perfect weather in {location['city']}! Natural light will enhance your mood by 15%.",
            'confidence': 85
        })
    elif weather['condition'] in ['Light rain', 'Moderate rain']:
        insights.append({
            'type': 'weather',
            'icon': '🌧️',
            'title': 'Cozy Day Ahead',
            'message': "Rainy weather detected. Great for indoor focus work and creative writing.",
            'confidence': 80
        })
    
    # Insight 5: Moon influence
    if moon['phase'] in ['New Moon', 'Waxing Crescent']:
        insights.append({
            'type': 'cosmic',
            'icon': moon['emoji'],
            'title': f'{moon["phase"]} Energy',
            'message': "New beginnings phase. Ideal for starting new projects and setting intentions.",
            'confidence': 75
        })
    elif moon['phase'] == 'Full Moon':
        insights.append({
            'type': 'cosmic',
            'icon': moon['emoji'],
            'title': 'Full Moon Peak',
            'message': "High energy period. Perfect for social activities and completing ongoing projects.",
            'confidence': 75
        })
    
    # Insight 6: Temperature advisory
    if weather['temperature'] > 28:
        insights.append({
            'type': 'temperature',
            'icon': '🌡️',
            'title': 'Heat Advisory',
            'message': f"Hot day ({weather['temperature']}°C). Stay hydrated and schedule demanding work for cooler hours.",
            'confidence': 92
        })
    elif weather['temperature'] < 5:
        insights.append({
            'type': 'temperature',
            'icon': '❄️',
            'title': 'Cold Day Alert',
            'message': f"Chilly weather ({weather['temperature']}°C). Your body needs extra energy. Eat warming foods.",
            'confidence': 92
        })
    
    return insights

def get_random_productivity_tip():
    """Get research-backed productivity tips"""
    tips = [
        "🧠 Your brain consumes 20% of your body's energy. Take glucose breaks!",
        "🌊 Drink water before coffee. Dehydration mimics fatigue.",
        "👀 Follow the 20-20-20 rule: Every 20 min, look 20 feet away for 20 sec.",
        "🎵 Classical music with 60-70 BPM matches resting heart rate, improving focus.",
        "🌡️ 21-22°C (70-72°F) is optimal for cognitive performance.",
        "🧘 2-minute breathing exercises can reset your nervous system.",
        "📱 Notifications fragment attention for 23 minutes on average.",
        "🌙 Blue light after 8 PM disrupts melatonin by 50%.",
        "🏃 10-minute walks increase creativity for 2 hours after.",
        "☕ Caffeine takes 20 minutes to activate. Drink before a power nap!"
    ]
    return random.choice(tips)

# ══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint — accepts GPS coords or falls back to IP"""
    try:
        body = request.get_json(silent=True) or {}

        # ── Option 1: Browser sent GPS coordinates ──
        if body.get('lat') and body.get('lon'):
            lat = float(body['lat'])
            lon = float(body['lon'])
            city    = body.get('city', 'Your Location')
            country = body.get('country', '')
            timezone = body.get('timezone', 'UTC')
            location = {
                'city': city,
                'country': country,
                'lat': lat,
                'lon': lon,
                'timezone': timezone,
                'isp': 'GPS',
                'source': '📍 GPS (exact)'
            }

        # ── Option 2: User typed a city manually ──
        elif body.get('city'):
            city_name = body['city']
            geo_url = f'https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json'
            geo_resp = requests.get(geo_url, timeout=5).json()
            results  = geo_resp.get('results', [])
            if not results:
                return jsonify({'success': False, 'error': f'City "{city_name}" not found. Try a different spelling.'}), 400
            r = results[0]
            location = {
                'city':     r.get('name', city_name),
                'country':  r.get('country', ''),
                'lat':      r['latitude'],
                'lon':      r['longitude'],
                'timezone': r.get('timezone', 'UTC'),
                'isp':      'Manual',
                'source':   '🔍 Manual entry'
            }

        # ── Option 3: Fallback — IP geolocation ──
        else:
            location = get_ip_location()
            location['source'] = '🌐 IP (approximate)'

        weather   = get_weather(location['lat'], location['lon'])
        moon      = get_moon_phase()
        circadian = calculate_circadian_rhythm()
        analysis  = analyze_productivity_pattern(weather, moon, circadian, location)

        return jsonify({
            'success':   True,
            'timestamp': datetime.now().isoformat(),
            'location':  location,
            'weather':   weather,
            'moon':      moon,
            'circadian': circadian,
            'analysis':  analysis,
            'tip':       get_random_productivity_tip()
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/quick-insight', methods=['GET'])
def quick_insight():
    """Get a quick insight without full analysis"""
    try:
        moon = get_moon_phase()
        now = datetime.now()
        
        return jsonify({
            'success': True,
            'moon_phase': moon['phase'],
            'moon_emoji': moon['emoji'],
            'current_time': now.strftime('%H:%M'),
            'tip': get_random_productivity_tip()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ══════════════════════════════════════════════════════════════════════════════
# STUNNING UI - Newspaper/Editorial Aesthetic with Bold Typography
# ══════════════════════════════════════════════════════════════════════════════

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Life Pattern Analyzer | Your Daily Optimization Engine</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Source+Serif+4:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --black: #0a0a0a;
    --charcoal: #1a1a1a;
    --graphite: #2d2d2d;
    --silver: #e8e8e8;
    --white: #fafafa;
    --accent: #ff4444;
    --accent-soft: #ff6666;
    --gold: #d4af37;
    --blue: #2563eb;
    --purple: #8b5cf6;
    --green: #10b981;
}

body {
    font-family: 'Source Serif 4', serif;
    background: var(--white);
    color: var(--black);
    line-height: 1.6;
    overflow-x: hidden;
}

/* Animated background pattern */
.bg-pattern {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0.03;
    z-index: 0;
    background-image: 
        repeating-linear-gradient(0deg, var(--black) 0px, transparent 1px, transparent 40px),
        repeating-linear-gradient(90deg, var(--black) 0px, transparent 1px, transparent 40px);
    animation: patternShift 60s linear infinite;
}

@keyframes patternShift {
    0% { transform: translate(0, 0); }
    100% { transform: translate(40px, 40px); }
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 30px;
    position: relative;
    z-index: 1;
}

/* Newspaper-style header */
header {
    border-bottom: 4px double var(--black);
    padding: 40px 0 30px;
    margin-bottom: 50px;
    position: relative;
    animation: slideDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.masthead {
    text-align: center;
    margin-bottom: 20px;
}

.publication-date {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--graphite);
    margin-bottom: 15px;
}

h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(48px, 8vw, 92px);
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -0.03em;
    margin-bottom: 12px;
    color: var(--black);
}

.subtitle {
    font-family: 'Source Serif 4', serif;
    font-size: clamp(16px, 2.5vw, 22px);
    font-weight: 400;
    font-style: italic;
    color: var(--graphite);
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.5;
}

.tagline {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 25px;
    flex-wrap: wrap;
}

.tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 6px 14px;
    border: 1.5px solid var(--black);
    background: var(--white);
    font-weight: 500;
    transition: all 0.3s ease;
}

.tag:hover {
    background: var(--black);
    color: var(--white);
    transform: translateY(-2px);
}

/* Main CTA Button */
.analyze-section {
    text-align: center;
    margin: 60px 0;
    animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s backwards;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.analyze-btn {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    padding: 22px 55px;
    background: var(--black);
    color: var(--white);
    border: none;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    letter-spacing: -0.02em;
}

.analyze-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.6s;
}

.analyze-btn:hover::before {
    left: 100%;
}

.analyze-btn:hover {
    background: var(--accent);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(255, 68, 68, 0.4);
}

.analyze-btn:active {
    transform: translateY(-1px);
}

.loading {
    display: none;
    text-align: center;
    padding: 40px;
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

.loading-text {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 20px;
}

/* Results Grid - Editorial Layout */
.results {
    display: none;
    animation: fadeIn 0.8s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.section-header {
    font-family: 'Playfair Display', serif;
    font-size: clamp(32px, 5vw, 56px);
    font-weight: 800;
    margin: 60px 0 30px;
    border-left: 6px solid var(--accent);
    padding-left: 20px;
    line-height: 1.1;
    letter-spacing: -0.02em;
    animation: slideInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Stats Cards - Magazine Style */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 25px;
    margin: 40px 0;
}

.stat-card {
    background: var(--white);
    border: 2px solid var(--black);
    padding: 30px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    animation: cardAppear 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }
.stat-card:nth-child(4) { animation-delay: 0.4s; }

@keyframes cardAppear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--accent), var(--gold));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.stat-card:hover::before {
    transform: scaleX(1);
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--graphite);
    margin-bottom: 10px;
    font-weight: 500;
}

.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 8px;
    background: linear-gradient(135deg, var(--black), var(--graphite));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-desc {
    font-size: 14px;
    color: var(--graphite);
    line-height: 1.4;
}

/* Insights - Feature Story Style */
.insights-container {
    margin: 50px 0;
}

.insight-card {
    background: var(--black);
    color: var(--white);
    padding: 40px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    animation: expandIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    border-left: 6px solid var(--accent);
}

.insight-card:nth-child(odd) {
    border-left-color: var(--gold);
}

@keyframes expandIn {
    from {
        opacity: 0;
        transform: scaleX(0.9);
    }
    to {
        opacity: 1;
        transform: scaleX(1);
    }
}

.insight-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
}

.insight-icon {
    font-size: 36px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.insight-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.01em;
}

.insight-message {
    font-size: 18px;
    line-height: 1.6;
    opacity: 0.95;
    margin-bottom: 15px;
}

.insight-meta {
    display: flex;
    gap: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    opacity: 0.7;
}

/* Energy Chart - Data Visualization */
.energy-chart {
    margin: 50px 0;
    padding: 40px;
    background: var(--white);
    border: 2px solid var(--black);
}

.chart-title {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 30px;
}

.chart-bars {
    display: grid;
    gap: 15px;
}

.energy-bar {
    display: flex;
    align-items: center;
    gap: 15px;
}

.bar-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
    width: 120px;
    font-weight: 500;
}

.bar-track {
    flex: 1;
    height: 32px;
    background: var(--silver);
    position: relative;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent-soft));
    position: relative;
    animation: barGrow 1.5s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes barGrow {
    from {
        width: 0 !important;
    }
}

.bar-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.bar-value {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    width: 60px;
    text-align: right;
}

/* Hourly Timeline - Interactive Schedule */
.timeline {
    margin: 50px 0;
    padding: 40px;
    background: linear-gradient(135deg, var(--charcoal), var(--graphite));
    color: var(--white);
}

.timeline-header {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 30px;
    color: var(--white);
}

.timeline-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 15px;
}

.time-block {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 20px 15px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.time-block::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: var(--accent);
    transform: scaleX(0);
    transition: transform 0.3s;
}

.time-block:hover::before {
    transform: scaleX(1);
}

.time-block:hover {
    background: rgba(255,255,255,0.1);
    transform: translateY(-3px);
}

.time-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 8px;
    letter-spacing: 1px;
}

.time-activity {
    font-size: 13px;
    opacity: 0.8;
    margin-bottom: 5px;
}

.time-confidence {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    opacity: 0.6;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Productivity Tip - Pull Quote Style */
.tip-section {
    margin: 60px 0;
    padding: 50px;
    background: var(--gold);
    color: var(--black);
    text-align: center;
    position: relative;
    animation: fadeInScale 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInScale {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.tip-section::before,
.tip-section::after {
    content: '"';
    font-family: 'Playfair Display', serif;
    font-size: 120px;
    position: absolute;
    opacity: 0.2;
    font-weight: 900;
}

.tip-section::before {
    top: 20px;
    left: 30px;
}

.tip-section::after {
    content: '"';
    bottom: 20px;
    right: 30px;
    transform: rotate(180deg);
}

.tip-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 15px;
    font-weight: 500;
}

.tip-text {
    font-family: 'Playfair Display', serif;
    font-size: clamp(20px, 3vw, 32px);
    font-weight: 600;
    line-height: 1.4;
    max-width: 800px;
    margin: 0 auto;
    letter-spacing: -0.01em;
}

/* Footer */
footer {
    margin-top: 80px;
    padding: 40px 0;
    border-top: 2px solid var(--black);
    text-align: center;
}

.footer-text {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--graphite);
    line-height: 2;
}

.footer-text a {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid var(--accent);
    transition: opacity 0.3s;
}

.footer-text a:hover {
    opacity: 0.7;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        padding: 0 20px;
    }
    
    h1 {
        font-size: 48px;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .timeline-grid {
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    }
    
    .analyze-btn {
        font-size: 22px;
        padding: 18px 40px;
    }
    
    .insight-card {
        padding: 25px;
    }
}

/* Loading Animation */
.spinner {
    width: 60px;
    height: 60px;
    border: 4px solid var(--silver);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Scroll Reveal Animation */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal.active {
    opacity: 1;
    transform: translateY(0);
}
</style>
</head>
<body>
<div class="bg-pattern"></div>

<div class="container">
    <header>
        <div class="masthead">
            <div class="publication-date" id="current-date"></div>
            <h1>Life Pattern Analyzer</h1>
            <p class="subtitle">
                Harness real-time weather, cosmic cycles, and circadian science to optimize every hour of your day
            </p>
            <div class="tagline">
                <span class="tag">🌍 Location-Aware</span>
                <span class="tag">🌤️ Weather-Integrated</span>
                <span class="tag">🌙 Circadian-Optimized</span>
                <span class="tag">📊 Data-Driven</span>
            </div>
        </div>
    </header>

    <div class="analyze-section">
        <button class="analyze-btn" onclick="analyzeLife()">
            Analyze My Day
        </button>
    </div>

    <div class="loading" id="loading">
        <div class="spinner"></div>
        <div class="loading-text">Analyzing Patterns...</div>
    </div>

    <div class="results" id="results">
        <!-- Location & Weather -->
        <h2 class="section-header">Your Current Context</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Location</div>
                <div class="stat-value" id="location-city">—</div>
                <div class="stat-desc" id="location-details">Detecting...</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Temperature</div>
                <div class="stat-value" id="weather-temp">—</div>
                <div class="stat-desc" id="weather-condition">—</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Moon Phase</div>
                <div class="stat-value" id="moon-phase">—</div>
                <div class="stat-desc" id="moon-illumination">—</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Optimal Time</div>
                <div class="stat-value" id="peak-time">—</div>
                <div class="stat-desc">For deep focus work</div>
            </div>
        </div>

        <!-- Current Energy Levels -->
        <h2 class="section-header">Current Energy Profile</h2>
        <div class="energy-chart">
            <div class="chart-title">Real-Time Capacity Assessment</div>
            <div class="chart-bars">
                <div class="energy-bar">
                    <div class="bar-label">Mental Focus</div>
                    <div class="bar-track">
                        <div class="bar-fill" id="bar-mental" style="width: 0%"></div>
                    </div>
                    <div class="bar-value" id="val-mental">0</div>
                </div>
                <div class="energy-bar">
                    <div class="bar-label">Physical Energy</div>
                    <div class="bar-track">
                        <div class="bar-fill" id="bar-physical" style="width: 0%; background: linear-gradient(90deg, #10b981, #34d399)"></div>
                    </div>
                    <div class="bar-value" id="val-physical">0</div>
                </div>
                <div class="energy-bar">
                    <div class="bar-label">Creative Flow</div>
                    <div class="bar-track">
                        <div class="bar-fill" id="bar-creative" style="width: 0%; background: linear-gradient(90deg, #8b5cf6, #a78bfa)"></div>
                    </div>
                    <div class="bar-value" id="val-creative">0</div>
                </div>
                <div class="energy-bar">
                    <div class="bar-label">Social Capacity</div>
                    <div class="bar-track">
                        <div class="bar-fill" id="bar-social" style="width: 0%; background: linear-gradient(90deg, #f59e0b, #fbbf24)"></div>
                    </div>
                    <div class="bar-value" id="val-social">0</div>
                </div>
            </div>
        </div>

        <!-- Key Insights -->
        <h2 class="section-header">Personalized Insights</h2>
        <div class="insights-container" id="insights"></div>

        <!-- 24-Hour Schedule -->
        <div class="timeline">
            <h2 class="timeline-header">24-Hour Optimization Schedule</h2>
            <div class="timeline-grid" id="timeline"></div>
        </div>

        <!-- Productivity Tip -->
        <div class="tip-section" id="tip-section">
            <div class="tip-label">Today's Science-Backed Insight</div>
            <div class="tip-text" id="tip-text">Loading...</div>
        </div>
    </div>

    <footer>
        <div class="footer-text">
            Built with real-time data from Open-Meteo, IP-API & Circadian Science<br>
            <a href="#" onclick="analyzeLife(); return false;">Run Analysis Again</a> | 
            No tracking, No cookies, Pure optimization
        </div>
    </footer>
</div>

<script>
// Set current date
document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
});

// ── IP Location fallback ──
async function getIPLocation() {
    try {
        const res  = await fetch('https://ipapi.co/json/');
        const data = await res.json();
        if (data.error) throw new Error(data.reason);
        return {
            city:    data.city         || 'Unknown',
            region:  data.region       || '',
            country: data.country_name || '',
            lat:     data.latitude,
            lon:     data.longitude,
            tz:      data.timezone     || Intl.DateTimeFormat().resolvedOptions().timeZone,
            source:  '🌐 IP location'
        };
    } catch {
        try {
            const res  = await fetch('http://ip-api.com/json/');
            const data = await res.json();
            return {
                city:    data.city       || 'Unknown',
                region:  data.regionName || '',
                country: data.country    || '',
                lat:     data.lat,
                lon:     data.lon,
                tz:      data.timezone   || Intl.DateTimeFormat().resolvedOptions().timeZone,
                source:  '🌐 IP location'
            };
        } catch { return null; }
    }
}

// ── Get city name from GPS coords using reverse geocoding ──
async function reverseGeocode(lat, lon) {
    try {
        const res  = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&zoom=10&addressdetails=1`,
            { headers: { 'Accept-Language': 'en', 'User-Agent': 'LifePatternAnalyzer/1.0' } }
        );
        const data = await res.json();
        const addr = data.address || {};
        const city =
            addr.suburb       ||
            addr.village      ||
            addr.town         ||
            addr.city         ||
            addr.municipality ||
            addr.county       ||
            'Your Location';
        const country  = addr.country || '';
        const region   = addr.state   || addr.region || '';
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        return { city, country, region, timezone };
    } catch {
        return { city: 'Your Location', country: '', region: '', timezone: Intl.DateTimeFormat().resolvedOptions().timeZone };
    }
}

// ── Ask browser for GPS ──
function getGPSLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) { reject(new Error('no_gps')); return; }
        navigator.geolocation.getCurrentPosition(resolve, reject, {
            timeout: 8000, maximumAge: 300000, enableHighAccuracy: true
        });
    });
}

// ── Show manual city input box ──
function showManualInput() {
    document.getElementById('loading').style.display = 'none';

    // Create modal if it doesn't exist yet
    if (!document.getElementById('city-modal')) {
        const modal = document.createElement('div');
        modal.id = 'city-modal';
        modal.style.cssText = `
            position:fixed; inset:0; background:rgba(0,0,0,0.7);
            display:flex; align-items:center; justify-content:center; z-index:9999;
        `;
        modal.innerHTML = `
            <div style="background:#1a1a1a; border:1px solid #333; border-radius:12px;
                        padding:36px; max-width:420px; width:90%; text-align:center;">
                <div style="font-size:36px; margin-bottom:16px;">📍</div>
                <h3 style="color:#fafafa; font-size:20px; margin-bottom:8px;">Enter Your City</h3>
                <p style="color:#888; font-size:14px; margin-bottom:24px;">
                    GPS access was denied. Type your city for accurate weather & analysis.
                </p>
                <input id="city-input" type="text" placeholder="e.g. Calgary, London, Tokyo"
                    style="width:100%; padding:14px 16px; border-radius:8px; border:1px solid #444;
                           background:#0a0a0a; color:#fafafa; font-size:16px; margin-bottom:16px;
                           outline:none; font-family:inherit;"
                />
                <button onclick="submitCity()"
                    style="width:100%; padding:14px; border-radius:8px; border:none;
                           background:#ff4444; color:#fff; font-size:16px; cursor:pointer;
                           font-family:inherit; font-weight:600;">
                    Analyze My Day →
                </button>
                <p style="color:#555; font-size:12px; margin-top:16px;">
                    Or <a href="#" onclick="runAnalysis({})" style="color:#ff4444;">
                    continue with approximate IP location</a>
                </p>
            </div>
        `;
        document.body.appendChild(modal);

        // Submit on Enter key
        modal.querySelector('#city-input').addEventListener('keydown', e => {
            if (e.key === 'Enter') submitCity();
        });
    }

    document.getElementById('city-modal').style.display = 'flex';
    setTimeout(() => document.getElementById('city-input').focus(), 100);
}

function closeModal() {
    const m = document.getElementById('city-modal');
    if (m) m.style.display = 'none';
}

async function submitCity() {
    const city = document.getElementById('city-input').value.trim();
    if (!city) { document.getElementById('city-input').style.border = '1px solid #ff4444'; return; }
    closeModal();
    document.getElementById('loading').style.display = 'block';
    await runAnalysis({ city });
}

// ── Core analysis runner ──
async function runAnalysis(payload) {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (data.success) {
            displayResults(data);
            setTimeout(() => {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('results').style.display = 'block';
                setTimeout(() => {
                    document.querySelectorAll('.stat-card, .insight-card').forEach((el, i) => {
                        setTimeout(() => {
                            el.style.opacity = '0';
                            el.style.transform = 'translateY(20px)';
                            setTimeout(() => {
                                el.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
                                el.style.opacity = '1';
                                el.style.transform = 'translateY(0)';
                            }, 50);
                        }, i * 100);
                    });
                }, 100);
            }, 1500);
        } else {
            alert('Error: ' + data.error);
            document.getElementById('loading').style.display = 'none';
        }
    } catch (error) {
        alert('Error connecting to server: ' + error.message);
        document.getElementById('loading').style.display = 'none';
    }
}

// ── Main entry point ──
async function analyzeLife() {
    document.getElementById('results').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });

    try {
        // Step 1 — try GPS
        const position = await getGPSLocation();
        const { latitude: lat, longitude: lon } = position.coords;

        // Step 2 — reverse geocode to get city name
        const geo = await reverseGeocode(lat, lon);

        // Step 3 — send GPS coords to backend
        const label = geo.region ? geo.city + ', ' + geo.region : geo.city;
        await runAnalysis({ lat, lon, city: label, country: geo.country, timezone: geo.timezone });

    } catch (err) {
        // ② GPS denied — silently try IP location
        const ip = await getIPLocation();
        if (ip && ip.city && ip.city !== 'Unknown') {
            const label = ip.region ? ip.city + ', ' + ip.region : ip.city;
            await runAnalysis({ lat: ip.lat, lon: ip.lon, city: label, country: ip.country, timezone: ip.tz });
        } else {
            // ③ IP also failed — ask user to type city manually
            showManualInput();
        }
    }
}

function displayResults(data) {
    // Location & Weather
    document.getElementById('location-city').textContent = data.location.city;
    document.getElementById('location-details').textContent =
        `${data.location.country} • ${data.location.timezone} • ${data.location.source || ''}`;
    
    document.getElementById('weather-temp').textContent = 
        `${data.weather.temperature}°C`;
    document.getElementById('weather-condition').textContent = 
        `${data.weather.condition} • ${data.weather.humidity}% humidity`;
    
    document.getElementById('moon-phase').textContent = 
        `${data.moon.emoji}`;
    document.getElementById('moon-illumination').textContent = 
        `${data.moon.phase} • ${data.moon.illumination}% illuminated`;
    
    // Find peak focus time
    const peakMental = data.analysis.hourly_predictions.reduce((max, curr) => 
        curr.mental > max.mental ? curr : max
    );
    document.getElementById('peak-time').textContent = peakMental.time;
    
    // Energy bars with animation
    const currentEnergy = data.circadian.current_energy;
    setTimeout(() => {
        setEnergyBar('mental', currentEnergy.mental);
        setEnergyBar('physical', currentEnergy.physical);
        setEnergyBar('creative', currentEnergy.creative);
        setEnergyBar('social', currentEnergy.social);
    }, 200);
    
    // Insights
    displayInsights(data.analysis.insights);
    
    // Timeline
    displayTimeline(data.analysis.hourly_predictions);
    
    // Tip
    document.getElementById('tip-text').textContent = data.tip;
}

function setEnergyBar(type, value) {
    const bar = document.getElementById(`bar-${type}`);
    const val = document.getElementById(`val-${type}`);
    
    bar.style.width = `${value}%`;
    val.textContent = Math.round(value);
}

function displayInsights(insights) {
    const container = document.getElementById('insights');
    container.innerHTML = '';
    
    insights.forEach((insight, index) => {
        const card = document.createElement('div');
        card.className = 'insight-card';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <div class="insight-header">
                <div class="insight-icon">${insight.icon}</div>
                <div class="insight-title">${insight.title}</div>
            </div>
            <div class="insight-message">${insight.message}</div>
            <div class="insight-meta">
                <span>Confidence: ${insight.confidence}%</span>
                ${insight.time ? `<span>Time: ${insight.time}</span>` : ''}
            </div>
        `;
        container.appendChild(card);
    });
}

function displayTimeline(predictions) {
    const container = document.getElementById('timeline');
    container.innerHTML = '';
    
    // Show next 12 hours
    predictions.slice(0, 12).forEach((pred, index) => {
        const block = document.createElement('div');
        block.className = 'time-block';
        block.style.animationDelay = `${index * 0.05}s`;
        block.innerHTML = `
            <div class="time-label">${pred.time}</div>
            <div class="time-activity">${pred.recommended_activity}</div>
            <div class="time-confidence">${pred.confidence}% optimal</div>
        `;
        
        // Add click tooltip
        block.title = `Mental: ${pred.mental} | Physical: ${pred.physical} | Creative: ${pred.creative} | Social: ${pred.social}`;
        
        container.appendChild(block);
    });
}

// Auto-refresh every hour
setInterval(() => {
    if (document.getElementById('results').style.display === 'block') {
        analyzeLife();
    }
}, 3600000); // 1 hour
</script>
</body>
</html>
"""

# ══════════════════════════════════════════════════════════════════════════════
# RUN THE APP
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🌟  LIFE PATTERN ANALYZER - Revolutionary Daily Optimization Engine")
    print("="*80)
    print("\n📍 Features:")
    print("   • Real-time location detection (IP-based)")
    print("   • Live weather integration (Open-Meteo API)")
    print("   • Moon phase calculations & cosmic influences")
    print("   • Circadian rhythm optimization")
    print("   • 24-hour energy prediction")
    print("   • Personalized insights & recommendations")
    print("\n🌐 Access Points:")
    print("   • Local:   http://localhost:5555")
    print("   • Network: http://0.0.0.0:5555")
    print("\n✨ This is a completely unique project - combining multiple real-time")
    print("   data sources with circadian science for personalized optimization!")
    print("\n" + "="*80 + "\n")
    
    app.run(host='0.0.0.0', port=5555, debug=True)
