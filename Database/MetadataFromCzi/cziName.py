import re


class Name:
    def __init__(self, name):
        self.name = name
        self.mouseId = self.setMouseId()
        self.viralVectors = self.setViralVectors()
        self.tags = self.setTags()
        self.injectionSite = self.setInjectionSite()

    def exportAsDict(self):
        return {'name': self.name, 'mouse_id': self.mouseId, 'viral_vectors': self.formatViralVectors(),
                'injection_site': self.injectionSite, 'tags': self.tags}

    def setMouseId(self):
        # Pattern is s followed by 1 to 4 digits and ignoring lower or upper case.
        # Return the digits.
        try:
            return re.search(r's\d{1,4}', self.name, re.IGNORECASE).group()[1:]
        except AttributeError:
            return 0

    def setViralVectors(self):
        try:
            vectors = []
            vectors.extend(self.findAAVVectors())
            vectors.extend(self.findRabVectors())
            return vectors
        except Exception:
            pass

    def formatViralVectors(self):
        if self.viralVectors:
            vectorLine = ''
            for vector in self.viralVectors:
                vectorLine += vector + ';'
            return vectorLine.rstrip(';')

    def findRabVectors(self):
        # We can have either rab#.# or rabv#.# so we try to find either patterns.
        try:
            return re.findall(r'(rabv?\d(?:\.\d))', self.name, re.IGNORECASE)
        except Exception:
            return []

    def findAAVVectors(self):
        # We can have either very distinct AAV### patterns or AAV###+### or AAV###-###.
        # We have to search for all three. AAV###-### and AAV###+### are splitted into different vectors and their
        # names are normalized to AAV###.
        try:
            AAVs = re.findall(r'AAV\d{3,4}[+-]\d{3,4}|AAV\d{3,4}', self.name, re.IGNORECASE)
            for AAV in AAVs:
                if re.search(r'[+-]', AAV):
                    splitAAV = re.compile(r'[+-]').split(AAV)
                    for i in range(len(splitAAV)):
                        if re.match(r'^\d{3,4}', splitAAV[i]):
                            splitAAV[i] = splitAAV[i].replace(splitAAV[i], 'AAV' + splitAAV[i])
                    AAVs.remove(AAV)
                    AAVs.extend(splitAAV)
            return AAVs
        except Exception:
            return []

    def setInjectionSite(self):
        try:
            return re.search(r'patte|IV', self.name, re.IGNORECASE).group()
        except Exception:
            return ''

    def setTags(self):
        try:
            tagLine = ''
            tags = re.findall(r'moelle|neurones|drg|BB|anti\s?mcherry|anti\s?rabbit|cre|cx3cr1', self.name, re.IGNORECASE)
            for tag in tags:
                trueTag = tag.replace(' ', '')
                if tagLine.find(trueTag) == -1:
                    tagLine += trueTag + ';'
            return tagLine.rstrip(';')
        except Exception:
            return []
