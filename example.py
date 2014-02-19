import onion

def tt(data):
    print 'tt'
    
def f1(data):
    print "F! Works"
    print data[0]
    print data[1]

onion.init('VMceXOHN','NfOBcqBFahPfHNjQ')
onion.get('/tt',tt)
onion.post('/f1',f1,'var1,var2')
print "Started..."
onion.start()

