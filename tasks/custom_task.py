import psutil
from datetime import datetime
import json
import os

def get_system_stats():
    stats = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return stats

def save_stats(stats):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Save to daily log file
    filename = f"logs/system_stats_{datetime.now().strftime('%Y-%m-%d')}.json"
    
    try:
        # Read existing data
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
        else:
            data = []
        
        # Append new stats
        data.append(stats)
        
        # Write back to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving stats: {str(e)}")
        return False

def execute():
    try:
        print(f"\n[{datetime.now()}] Running system health check...")
        
        # Get system statistics
        stats = get_system_stats()
        
        # Print current stats
        print(f"CPU Usage: {stats['cpu_percent']}%")
        print(f"Memory Usage: {stats['memory_percent']}%")
        print(f"Disk Usage: {stats['disk_usage']}%")
        print(f"Battery Level: {stats['battery']}%")
        
        # Save stats to file
        if save_stats(stats):
            print("Stats saved successfully!")
        else:
            print("Failed to save stats!")
        
        # Check for warning conditions
        if stats['cpu_percent'] > 80:
            print("⚠️ WARNING: High CPU usage detected!")
        if stats['memory_percent'] > 80:
            print("⚠️ WARNING: High memory usage detected!")
        if stats['disk_usage'] > 80:
            print("⚠️ WARNING: High disk usage detected!")
        if isinstance(stats['battery'], (int, float)) and stats['battery'] < 20:
            print("⚠️ WARNING: Low battery level!")
            
    except Exception as e:
        print(f"Error in system health check: {str(e)}")

if __name__ == "__main__":
    # Test the task
    execute() 