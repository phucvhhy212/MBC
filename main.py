import json
from pydifact.segmentcollection import Interchange
from pydifact.process import ProcessEDI

interchange = Interchange.from_file('./pydifact/cargo.txt')
process = ProcessEDI()
final_res = {}
current_json = {}
current_tag = ""
count_repeat = 1


##### HANDLE SEGMENT GROUP ##########

segment_group_keys = []

############
for segment in interchange.segments[9:13]:
    match segment.tag:
        case "UNH":
            keys = ["MESSAGE_REFERENCE_NUMBER","MESSAGE_IDENTIFIER"]
            child_keys = [["MESSAGE_TYPE_IDENTIFIER","MESSAGE_TYPE_VERSION_NUMBER","MESSAGE_TYPE_RELEASE_NUMBER","CONTROLLING_AGENCY","ASSOCIATION_ASSIGNED_CODE"]]
            max_use = 1
        case "BGM":
            keys = ["DOCUMENT/MESSAGE_NAME","DOCUMENT/MESSAGE_IDENTIFICATION","MESSAGE_FUNCTION_CODE","RESPONSE_TYPE_CODE"]
            child_keys = [["DOCUMENT_NAME_CODE","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE","DOCUMENT_NAME"],["DOCUMENT/MESSAGE_NUMBER","VERSION"]]
            max_use = 1
        case "CTA":
            keys = ["CONTACT_FUNCTION_CODE","DEPARTMENT_OR_EMPLOYEE_DETAILS"]
            child_keys = [["DEPARTMENT_OR_EMPLOYEE_IDENTIFICATION","DEPARTMENT_OR_EMPLOYEE"]]
            max_use = 1
        case "COM":
            keys = ["COMMUNICATION_CONTACT"]
            child_keys = [["COMMUNICATION_NUMBER","COMMUNICATION_NUMBER_CODE_QUALIFIER"]]
            max_use = 9
        case "DTM":
            keys = ["DATE/TIME/PERIOD"]
            child_keys = [["DATE/TIME/PERIOD_FUNCTION_CODE_QUALIFIER","DATE/TIME/PERIOD_VALUE","DATE/TIME/PERIOD_FORMAT_CODE"]]
            max_use = 3
        case "TSR":
            keys = ["CONTRACT_AND_CARRIAGE_CONDITION"]
            child_keys = [["CONTRACT_AND_CARRIAGE_CONDITION_CODE"]]
            max_use = 1
        case "FTX":
            keys = ["TEXT_SUBJECT_CODE_QUALIFIER","TEXT_FUNCTION_CODED","TEXT_REFERENCE","TEXT_LITERAL"]
            child_keys = [["FREE_TEXT_VALUE_CODE","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE"],["FREE_TEXT_VALUE"]]
            max_use = 22
        case "GDS":
            keys = ["NATURE_OF_CARGO"]
            child_keys = [["NATURE_OF_CARGO_CODED"]]
            max_use = 4
        case "LOC":
            keys = ["LOCATION_FUNCTION_CODE_QUALIFIER","LOCATION_IDENTIFICATION","RELATED_LOCATION_ONE_IDENTIFICATION","RELATED_LOCATION_TWO_IDENTIFICATION"]
            child_keys = [["LOCATION_NAME_CODE","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE","LOCATION_NAME"],["RELATED_PLACE/LOCATION_ONE_IDENTIFICATION","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE","RELATED_PLACE/LOCATION_ONE"]]
            max_use = 89
            
    
    json_segment = process.processSegment(keys,child_keys,segment)
    segment_group_keys.append(json_segment)
    # if the next line of the message has the same tag with the previous one, append both in the final_res
    if current_tag == segment.tag:
        count_repeat +=1
        if(count_repeat > max_use):
            raise Exception(f"Maximum repeat on segment {segment.tag}")
        if not isinstance(final_res[segment.tag],list):
            final_res[segment.tag] = [json_segment["elements"], current_json["elements"]]
        else:
            final_res[segment.tag].append(json_segment["elements"])
    else:
        final_res[segment.tag] = json_segment["elements"]
        count_repeat = 1
    current_json = json_segment
    current_tag = segment.tag
    # print("=====================")
    # print(json.dumps(final_res,indent=2))
    
seg1 = process.process_segment1(segment_group_keys)
print(json.dumps(seg1,indent=2))
        