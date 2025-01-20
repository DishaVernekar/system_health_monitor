import psutil
import logging
import time

# Define thresholds
CPU_THRESHOLD = 80  # CPU usage > 80%
MEMORY_THRESHOLD = 80  # Memory usage > 80%
DISK_THRESHOLD = 90  # Disk usage > 90%

# Set up logging
logging.basicConfig(filename='/var/log/system_health.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        alert_message = f"CPU usage is high: {cpu_usage}%"
        print(alert_message)
        logging.warning(alert_message)

def check_memory_usage():
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD:
        alert_message = f"Memory usage is high: {memory.percent}%"
        print(alert_message)
        logging.warning(alert_message)

def check_disk_usage():
    disk = psutil.disk_usage('/')
    if disk.percent > DISK_THRESHOLD:
        alert_message = f"Disk usage is high: {disk.percent}%"
        print(alert_message)
        logging.warning(alert_message)

def check_processes():
    # Check if there are any processes consuming high CPU
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc.cpu_percent(interval=1)  # Initialize CPU percent calculation
            if proc.cpu_percent() > 50:  # Threshold for high CPU usage per process
                alert_message = f"Process {proc.info['name']} (PID: {proc.info['pid']}) is using high CPU: {proc.info['cpu_percent']}%"
                print(alert_message)
                logging.warning(alert_message)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def monitor_system():
    while True:
        check_cpu_usage()
        check_memory_usage()
        check_disk_usage()
        check_processes()
        
        # Sleep for a minute before the next check
        time.sleep(60)

if __name__ == '__main__':
    print("System health monitoring started...")
    monitor_system()
