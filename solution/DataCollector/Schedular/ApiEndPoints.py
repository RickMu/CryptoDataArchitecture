from enum import Enum
class EndPointProviders (Enum):
    Gdx = 1
    EC2 = 2

class EndPoints:
    endPoints = {
        EndPointProviders.Gdx: "https://api.gdax.com",
        EndPointProviders.EC2: 'http://ec2-35-169-63-106.compute-1.amazonaws.com'
    }