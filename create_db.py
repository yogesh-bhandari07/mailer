from email.mime import base
from operator import imod
from database import Base,engine
import models
print('Connecting.....')
Base.metadata.create_all(engine)
