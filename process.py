import json


class ProcessEDI:
    segments_group_1 = ["LOC","DTM"]
    segments_group_2 = ["RFF","DTM"]
    segments_group_4 = {"segments_group_4":["LOC","DTM"]}
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
    
    
    
    def isInSegmentGroup(self,segment):
        """Check if the message has reached the segment group or not (tag not in the first 10 segments of the message)
        """
        if self.start_segment_group:
            return True
        else:        
            self.start_segment_group =  segment.tag not in ["","UNB","UNH","BGM","CTA","COM","DTM","TSR","FTX","FTX","GDS"]
        return self.start_segment_group
    
    def findSegmentGroup(self,segment,segment_group_tags:list[dict]):
        """Find the index of the segment group which the segment in
        
            :param segment: The segment to find
            :param segment_group_tags: list of tags in all segment groups
            :returns: the segment group found or None
        """
        for segment_group_keys_item in segment_group_tags:
            if self.pass_sg_index !=0 and segment_group_tags.index(segment_group_keys_item) < self.pass_sg_index: continue
            flat_array = [item for value in segment_group_keys_item.values() for sublist in (value if isinstance(value, list) else [value]) for item in (sublist if isinstance(sublist, list) else [sublist])]
            if segment.tag in flat_array:
                # return {"index":self.segment_group_dict_keys.index(segment_group_keys_item),"key":next(iter(segment_group_keys_item))}
                return segment_group_keys_item
        return None
    
    def convertSegmentMessageToDict(self,keys,child_keys,segment):
        """Convert the segment's element to dictionary format.
        
            :param keys: main elements of the segment
            :param child_keys: sub-elements of the segment (a main elements can contain sub-elements)
            :param segment: the segment to process
            :returns: The dictionary formatted of the segment
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
    
    def processSegmentGroup(self,segment_array:list,segment_group_tags:list):
        final_res = {}
        final_array = []
        final_array_item = {}
        segment_group_name = next(iter(segment_group_tags))
        key = segment_group_tags[segment_group_name][0]
        for segment in segment_array:
            # if segment's tag is the sg key
            if segment["tag"] == key:
                if final_array_item.get(key) is None:
                    final_array_item[key] = segment["elements"]
                # a segment tag's key value already exist => segment group has been repeated
                else:
                    final_array.append(final_array_item)
                    final_array_item = {}
                    final_array_item[key] = segment["elements"]
            else:
                for tag_element in segment_group_tags:
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
                case "GID":
                    keys = ["GOODS_ITEM_NUMBER","NUMBER_AND_TYPE_OF_PACKAGES"]
                    child_keys = [["NUMBER_OF_PACKAGES","PACKAGE_TYPE_DESCRIPTION_CODE","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE","TYPE_OF_PACKAGES"]]
                    max_use = 4
                case "MEA":
                    keys = ["MEASUREMENT_ATTRIBUTE_CODE","MEASUREMENT_DETAILS","VALUE/RANGE"]
                    child_keys = [["MEASURED_ATTRIBUTE_CODE"],["MEASUREMENT_UNIT_CODE","MEASUREMENT_VALUE"]]
                    max_use = 4
                case "EQD":
                    keys = ["EQUIPMENT_TYPE_CODE_QUALIFIER","EQUIPMENT_IDENTIFICATION","EQUIPMENT_SIZE_AND_TYPE","EQUIPMENT_SUPPLIER,CODED","EQUIPMENT_STATUS_CODE","FULL/EMPTY_INDICATOR,CODED"]
                    child_keys = [["EQUIPMENT_IDENTIFICATION_NUMBER","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE","COUNTRY_NAME_CODE"],["EQUIPMENT_SIZE_AND_TYPE_DESCRIPTION_CODE","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE","EQUIPMENT_SIZE_AND_TYPE_DESCRIPTION"]]
                    max_use = 4
                case "EQN":
                    keys = ["NUMBER_OF_UNIT_DETAILS"]
                    child_keys = [["NUMBER_OF_UNITS","UNIT_TYPE_CODE_QUALIFIER"]]
                    max_use = 4
                case "TMD":
                    keys = ["MOVEMENT_TYPE","EQUIPMENT_PLAN","HAULAGE_ARRANGEMENTS,CODED"]
                    child_keys = [["MOVEMENT_TYPE_DESCRIPTION_CODE"]]
                    max_use = 4
                case "TMP":
                    keys = ["TEMPERATURE_QUALIFIER","TEMPERATURE_SETTING"]
                    child_keys = [["TEMPERATURE_SETTING","MEASUREMENT_UNIT_CODE"]]
                    max_use = 4
                case "UNT":
                    keys = ["NUMBER_OF_SEGMENTS_IN_A_MESSAGE","MESSAGE_REFERENCE_NUMBER"]
                    child_keys = [[]]
                    max_use = 4
                case "UNZ":
                    keys = ["INTERCHANGE_CONTROL_COUNT","INTERCHANGE_CONTROL_REFERENCE"]
                    child_keys = [[]]
                    max_use = 4             
            segment_dict = self.convertSegmentMessageToDict(keys,child_keys,segment)
            self.checkRepeat(segment,max_use)
            if self.isInSegmentGroup(segment):
                found_segment_group = self.findSegmentGroup(segment,self.segment_group_dict_keys)
                # tìm thấy sg, add segment vào mảng và tìm nốt những segment tiếp theo tương ứng để add
                if found_segment_group is not None:
                    found_segment_group_index = self.segment_group_dict_keys.index(found_segment_group)
                    # segment đang làm việc vẫn nằm trong group hiện tại
                    if found_segment_group_index == self.track_sg_index:
                        self.current_segment_group.append(segment_dict)
                    # segment đang làm việc nằm trong 1 group khác, xử lý group đằng trước
                    else:
                        segment_group_name = next(iter(self.segment_group_dict_keys[self.track_sg_index]))
                        if self.current_segment_group:
                            self.final_res[segment_group_name] = self.processSegmentGroup(self.current_segment_group,found_segment_group)
                            self.current_segment_group = [segment_dict]
                            self.pass_sg_index = found_segment_group_index
                        else:
                            self.current_segment_group.append(segment_dict)
                        self.track_sg_index = found_segment_group_index
                else:
                    self.start_segment_group = False
                    self.addDictToFinalJson(segment_dict)    
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
    