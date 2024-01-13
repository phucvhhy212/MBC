import json
from pydifact.segmentcollection import Interchange

from process import ProcessEDI


interchange = Interchange.from_file('./cargo.txt')
process = ProcessEDI()
final_res = process.processSegments(interchange.segments)
print(json.dumps(final_res,indent=2))

        
   