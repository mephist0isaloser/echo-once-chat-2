#function to generate a random port number
import random
def generate_port():
    return random.randint(1024, 49151)
PORT_ = generate_port()
#PORT = PORT_
print(PORT_)