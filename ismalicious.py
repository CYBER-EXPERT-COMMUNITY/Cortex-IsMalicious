#!/home/debian/myenv/ismalicious/bin/python


from cortexutils.analyzer import Analyzer
import requests

class IsMaliciousAnalyzer(Analyzer):
    

    def __init__(self):
        Analyzer.__init__(self)
        self.url = "https://api.ismalicious.com/check"
        self.service = self.get_param('config.service', None, 'Service parameter is missing')

    def summary(self, raw):
       # Analyzer.summary(self)
        taxonomies = []
        namespace = "CE"
        predicate = "IsMalicious"
        level = 'info'
        value = "N/A"

        if self.service == 'IsMalicious':
            value = raw['malicious']

            if value == True:
                 
                 level = 'suspicious'
        
        taxonomies.append(self.build_taxonomy(level, namespace, predicate, value))
        
        
        return {"taxonomies": taxonomies}
    
    def run(self):
        Analyzer.run(self)
        if self.service == 'IsMalicious' and (self.data_type == 'ip'or self.data_type == 'domain'): #(self.data_type == 'domain' or self.data_type == 'hash' or self.data_type == 'ip' or self.data_type == 'url' or self.data_type == 'user-agent'):
            try:

                type_artifact ="ip"
                if  self.data_type == 'domain' :
                     type_artifact ="domain"
                     
                response = requests.get(self.url+"?"+type_artifact+"="+self.get_data())
                result = response.json()
                self.report(result)
            except Exception as e:
                self.unexpectedError(e)
        
        else:
            self.notSupported()

if __name__ == '__main__':
    IsMaliciousAnalyzer().run()

