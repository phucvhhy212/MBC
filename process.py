import json


class ProcessEDI:
    segments_group_1 = ["LOC","DTM"]
    segments_group_2 = ["RFF","DTM"]
    segments_group_4 = ["LOC","DTM"]
    segments_group_3 = ["TDT",segments_group_4]
    segments_group_7 = ["CTA","COM"]
    segments_group_6 = ["NAD","LOC",segments_group_7]
    segments_group_11 = ["MEA"]
    segments_group_12 = ["DIM"]
    segments_group_13 = ["RFF","DTM"]
    segments_group_16 = ["CTA","COM"]
    segments_group_17 = ["MEA"]
    segments_group_15 = ["DGS","FTX",segments_group_16,segments_group_17]
    segments_group_9 = ["GID","FTX",segments_group_11,segments_group_12,segments_group_13,segments_group_15]
    segments_group_19 = ["NAD","DTM"]
    segments_group_18 = ["EQD","EQN","TMD","MEA","DIM","HAN","TMP","FTX","RFF",segments_group_19]

    segment_group_dict_keys = [{"segments_group_1":segments_group_1},{"segments_group_2":segments_group_2},{"segments_group_3":segments_group_3},{"segments_group_6":segments_group_6},{"segments_group_9":segments_group_9},{"segments_group_18":segments_group_18}]
    current_dict = {}
    count_repeat = 1
    final_res = {}
    start_segment_group = False
    current_tag = ""
    
    current_segment_group = []
    track_sg_index = 0
    pass_sg_index = 0
    def __init__(self) -> None:
        pass
    
    
    # DTM dang bi trung
    def isSegmentGroup(self,segment):
        if segment.tag == "DTM":
            if self.current_tag != segment.tag:
                self.start_segment_group = True
        else:        
            self.start_segment_group =  segment.tag not in ["","UNB","UNH","BGM","CTA","COM","DTM","TSR","FTX","FTX","GDS"]
        return self.start_segment_group
    
    def checkSegmentInGroup(self,segment,segment_group_keys:list[dict]):
        """Find the index of the segment group which the segment in
            :return: Ex {"index":1,"key":"segment_group1"}
        """
        for segment_group_keys_item in segment_group_keys:
            if self.pass_sg_index !=0 and segment_group_keys.index(segment_group_keys_item) < self.pass_sg_index: continue
            flat_array = [item for value in segment_group_keys_item.values() for sublist in (value if isinstance(value, list) else [value]) for item in (sublist if isinstance(sublist, list) else [sublist])]
            if segment.tag in flat_array:
                return {"index":self.segment_group_dict_keys.index(segment_group_keys_item),"key":next(iter(segment_group_keys_item))}
        return None
    
    def convertSegmentMessageToDict(self,keys,child_keys,segment):
        """Demonstrates triple double quotes
        docstrings and does nothing really.
        """
        segment_array = segment.elements
        count_list_item = 0
        segment_dict = {}
        for value in segment_array:
            if isinstance(value,list):
                segment_dict[keys[segment_array.index(value)]] = dict(zip(child_keys[count_list_item],value))
                count_list_item += 1
            else:
                segment_dict[keys[segment_array.index(value)]] = value
        segment_dict = {"tag": f"{segment.tag}","elements":segment_dict}
        return segment_dict
    
    def process_segment1(self,segment_array:list,key,segment_group_name):
        final_res = {}
        final_array = []
        final_array_item = {}
        for segment in segment_array:
            if segment["tag"] == key:
                if final_array_item.get(key) is None:
                    final_array_item[key] = segment["elements"]
                # a segment tag's key value already exist => segment group has been repeated
                else:
                    final_array.append(final_array_item)
                    final_array_item = {}
                    final_array_item[key] = segment["elements"]
            else:
                if final_array_item.get(segment["tag"]) is None:
                    final_array_item[segment["tag"]] = segment["elements"]
                else:
                    if isinstance(final_array_item[segment["tag"]],dict):
                        final_array_item[segment["tag"]] = [final_array_item[segment["tag"]],segment["elements"]]
                    elif isinstance(final_array_item["DTM"],list) :
                        final_array_item[segment["tag"]].append(segment["elements"])
        if len(final_array_item) != 0:
            final_array.append(final_array_item)
        final_res[segment_group_name]= final_array
        return final_res
    
    def processSegments(self,segment_array:list):
        for segment in segment_array:
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
                    max_use = 1
                case "RFF":
                    keys = ["REFERENCE"]
                    child_keys = [["REFERENCE_FUNCTION_CODE_QUALIFIER","REFERENCE_IDENTIFIER"]]
                    max_use = 2
                case "TDT":
                    keys = ["TRANSPORT_STAGE_CODE_QUALIFIER","CONVEYANCE_REFERENCE_NUMBER","MODE_OF_TRANSPORT","TRANSPORT_MEANS","CARRIER","TRANSIT_DIRECTION_INDICATOR_CODE","EXCESS_TRANSPORTATION_INFORMATION","TRANSPORT_IDENTIFICATION"]
                    child_keys = [["TRANSPORT_MODE_NAME_CODE"],["TRANSPORT_MEANS_DESCRIPTION_CODE","TRANSPORT_MEANS_DESCRIPTION"],["CARRIER_IDENTIFICATION","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE"],["TRANSPORT_MEANS_IDENTIFICATION_NAME_IDENTIFIER","CODE_LIST_RESPONSIBLE_AGENCY_CODE","TRANSPORT_MENAS_IDENTIFICATION_NAME","NATIONALITY_OF_MEANS_OF_TRANSPORT_CODED"]]
                    max_use = 2
                case "NAD":
                    keys = ["PARTY_FUNCTION_CODE_QUALIFIER","PARTY_IDENTIFICATION_DETAILS","NAME_AND_ADDRESS","PARTY_NAME","STREET","CITY_NAME","COUNTRY_SUB-ENTITY_DETAILS","POSTAL_IDENTIFICATION_CODE","COUNTRY_NAME_CODE"]
                    child_keys = [["PARTY_IDENTIFIER","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE"],["NAME_AND_ADDRESS_LINE","NAME_AND_ADDRESS_LINE","NAME_AND_ADDRESS_LINE","NAME_AND_ADDRESS_LINE","NAME_AND_ADDRESS_LINE"],["PARTY_NAME","PARTY_NAME","PARTY_NAME","PARTY_NAME","PARTY_NAME","PARTY_NAME_FORMAT_CODE"],["STREET_AND_NUMBER/P.O._BOX","STREET_AND_NUMBER/P.O._BOX","STREET_AND_NUMBER/P.O._BOX","STREET_AND_NUMBER/P.O._BOX","STREET_AND_NUMBER/P.O._BOX"],["COUNTRY_SUB_ENTITY_NAME_CODE","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE","COUNTRY_SUB-ENTITY_NAME"]]
                    max_use = 4              
            segment_dict = self.convertSegmentMessageToDict(keys,child_keys,segment)
            self.checkRepeat(segment,max_use)
            if self.isSegmentGroup(segment):
                found_segment_group = self.checkSegmentInGroup(segment,self.segment_group_dict_keys)
                # tìm thấy sg, add segment vào mảng và tìm nốt những segment tiếp theo tương ứng để add
                if found_segment_group is not None:
                    # segment đang làm việc vẫn nằm trong group hiện tại
                    if found_segment_group["index"] == self.track_sg_index:
                        self.current_segment_group.append(segment_dict)
                    # segment đang làm việc nằm trong 1 group khác, xử lý group đằng trước
                    else:
                        segment_group_name = next(iter(self.segment_group_dict_keys[self.track_sg_index]))
                        if self.current_segment_group:
                            self.final_res[segment_group_name] = self.process_segment1(self.current_segment_group,self.segment_group_dict_keys[self.track_sg_index][segment_group_name][0],segment_group_name)
                            self.current_segment_group = [segment_dict]
                            self.pass_sg_index = found_segment_group["index"]
                        else:
                            self.current_segment_group.append(segment_dict)
                        self.track_sg_index = found_segment_group["index"]
            else:
                self.addDictToFinalJson(segment_dict)
        return self.final_res
            
                        
                
    def checkRepeat(self,segment,max_use):
        if self.current_tag == segment.tag:
            self.count_repeat +=1
        else:
            self.count_repeat = 1
        if(self.count_repeat > max_use):
            raise Exception(f"Maximum repeat on segment {segment.tag}")
    
    
    def addDictToFinalJson(self,segment_dict):
        tag = segment_dict["tag"]
        elements = segment_dict["elements"]
        # if final_res already having a segment with the same tag with the current processing segment, add to list
        if self.count_repeat > 1: 
            if not isinstance(self.final_res[tag],list):
                self.final_res[tag] = [elements, self.current_dict]
            else:
                self.final_res[tag].append(elements)
        else:
            self.final_res[tag] = elements
        self.current_dict = elements
        self.current_tag = tag
        print("=======================================================================")
        print(json.dumps(self.final_res,indent=2))