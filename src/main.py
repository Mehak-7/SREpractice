import psutil
import smtplib
from email.mime.text import MIMEText
from configparser import ConfigParser
import time


#this function will collect system metrics 
def collect_system_metrics():
    #getting the CPU usage, and adding an interval of 10, so cpu_percent() function
    #will collect the CPU usage every 10 seconds
    cpu_usage = psutil.cpu_percent(interval=10)

    #getting the memory usage
    mem_usage = psutil.virtual_memory().percent

    #getting the disk usage
    disk_usage = psutil.disk_usage('/').percent

    print("Collecting system metrics...")

    return cpu_usage,mem_usage,disk_usage

#this function will send the email alerts using the MIMEText
def send_alert(metric, threshold):
    #creating a message object
    message = MIMEText(f"Metric {metric} exceeded the threshold of {threshold})%")
    
    #Setting the subject for this email, based on respective metric being reported
    message['Subject'] = f"Alert: {metric} threshold exceeded"
    
    #sender and reciever emails (changed to hide personal information)
    message['From'] = 'abc@example.com'
    message['To'] = 'xyz@example.com'

    print(f"Sending email alert for {metric}...")

    # Read the configuration file
    config = ConfigParser()
    config.read('config.ini')
    smtp_config = config['SMTP']

    # Get the SMTP details from the configuration, here didn't add details
    #all details are in config.ini file which is in .gitignore, so as to hide sensitive information
    smtp_host = smtp_config['host']
    smtp_port = int(smtp_config['port'])
    smtp_username = smtp_config['username']
    smtp_password = smtp_config['password']

    #trying to send the email
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            # smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(message)
    except Exception as e:
        print(f"Error: email could not be sent: {e}")



# Main monitoring loop
def monitor():
    cpu_threshold = 30  # Example threshold for CPU usage (Reduced for testing)
    mem_threshold = 50  # Example threshold for memory usage (Reduced for testing)
    disk_threshold = 40  # Example threshold for disk usage (Reduced for testing)

    #setting the monitoring timeout, ideally should be 3600 i.e. an hour to keep a check
    #also reduced this for testing
    timeout = 10

    #starting the monitoring process
    start_time = time.time()
    
    #loop checking when monitoring timeout has not been reached
    while time.time() - start_time < timeout:

        #collecting the respective information
        cpu_usage, mem_usage, disk_usage = collect_system_metrics()

        #if the threshold is reached, an alert through email is sent
        if cpu_usage > cpu_threshold:
            send_alert('CPU', cpu_threshold)
        
        if mem_usage > mem_threshold:
            send_alert('Memory', mem_threshold)
        
        if disk_usage > disk_threshold:
            send_alert('Disk', disk_threshold)

        #sleep for 10 seconds
        time.sleep(10)
    
        #this is the case when monitoring time out has been reached
        if time.time() - start_time >= timeout:
            print("Monitoring timeout reached. Exiting...")
            break

# Start the monitoring process
monitor()



