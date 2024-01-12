import json
from pydifact.segmentcollection import Interchange

from process import ProcessEDI


interchange = Interchange.from_file('./cargo.txt')
process = ProcessEDI()
process.processSegments(interchange.segments)

        
   