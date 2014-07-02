import client
def print_stuff(params):
    print "The Client Works!!",
    print params["state"]
client.declare(print_stuff,"testfunc")
client.loop()
