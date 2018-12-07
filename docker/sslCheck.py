import ssl
import socket
from datetime import datetime, date

def getNotAfterDate(site):
    port = '443'

    context = ssl.create_default_context()
    with socket.create_connection((site, port)) as sock:
        with context.wrap_socket(sock, server_hostname=site) as ssock:
            data = ssock.getpeercert()
    
    dt = (datetime.strptime(data['notAfter'], '%b %d %H:%M:%S %Y %Z'))
    return dt.date()

def certDaysRemaining(site):
    today = date.today()
    try:
        certNotAfterDate = getNotAfterDate(site)
        daysRemaining = certNotAfterDate - today
        return daysRemaining.days
    except Exception as e:
        print('\nA certificate check is failing, {0:s} is not valid:'.format(site))
        print(e)
        print('\n')
        return -1