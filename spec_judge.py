class spec_judge:
    def __init__(self):
        self.names = []

    def check(self,names):
        self.names = names
        outputs = []
        result = []
        for i in self.names:
            f = open('out/' + i + '.out','r')
            result.append(0)
            outputs.append(f)
        s = '1'
        t = True
        while s != '':
            s = outputs[0].readline().strip()
            for i in range(1,len(self.names)):
                if s != outputs[i].readline().strip():
                    if (result[i] == 0):
                        result[i] = -1
                        print('\t' + self.names[i] + ' : WA')
                    t = False
        for i in outputs:
            i.close()
        for i in range(0,len(self.names)):
                if (result[i] == 0):
                    print('\t'+ self.names[i] + ' : AC')
        return t

    def run(self,names):
        if (names == []):
            return True
        r = self.check(names)
        return r
