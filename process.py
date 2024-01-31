import json


class ProcessEDI:
    segment_group = {
        "LOC": ["LOC","DTM"],
        "RFF": ["RFF","DTM"],
        "TDT": ["TDT","LOC","DTM"],
        "NAD": ["NAD","CTA","COM","DTM"],
        "DIM": ["DIM"],
        "CTA": ["CTA","COM"],
        "MEA": ["MEA"],
        "DGS": ["DGS","FTX","CTA","COM","MEA"],
        "GID": ["GID","FTX","MEA","DIM","RFF","DTM","DGS","FTX","CTA","COM","MEA"],
        "EQD": ["EQD","EQN","TMD","MEA","DIM","HAN","TMP","FTX","RFF","NAD","DTM"]
    }

    current_dict = {}
    count_repeat = 1
    final_res = {}
    start_segment_group = False
    current_tag = ""
    current_segment_group = []
    current_segment_group_elements = []
    track_segment_group= 0
    # pass_sg_index = 0
    max_use = 1
    def __init__(self) -> None:
        pass
    
    def _UNH(self,segment) -> dict:
        keys = ["message_reference_number","message_identifier"]
        child_keys = [["messeage_type_identifier","messeage_type_version_number","messeage_type_release_number","controlling_agency",
                       "association_assigned_code"]]
        self.max_use = 1
        count_list_item = 0
        result = {}
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _BGM(self,segment) -> dict:
        keys = ["document/message_name","document/message_identification","message_function_code","response_type_code"]
        child_keys = [["document_name_code","code_list_identification_code","code_list_responsible_agency_code","document_name"],["document/message_number","version"]]
        self.max_use = 1
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _CTA(self,segment) -> dict:
        keys = ["contact_function_code","department_or_employee_details"]
        child_keys = [["department_or_employee_identification","department_or_employee"]]
        self.max_use = 1
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _COM(self,segment) -> dict:
        keys = ["communication_contact"]
        child_keys = [["communication_number","communication_number_code_qualifier"]]
        self.max_use = 9
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _DTM(self,segment) -> dict:
        keys = ["date/time/period"]
        child_keys = [["date/time/period_function_code_qualifier","date/time/period_value","date/time/period_format_code"]]
        self.max_use = 3
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _TSR(self,segment) -> dict:
        keys = ["contract_and_carriage_condition"]
        child_keys = [["contract_and_carriage_condition_code"]]
        self.max_use = 1
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _FTX(self,segment) -> dict:
        keys = ["TEXT_SUBJECT_CODE_QUALIFIER","TEXT_FUNCTION_CODED","TEXT_REFERENCE","TEXT_LITERAL"]
        child_keys = [["FREE_TEXT_VALUE_CODE","CODE_LIST_IDENTIFICATION_CODE","CODE_LIST_RESPONSIBLE_AGENCY_CODE"],["FREE_TEXT_VALUE"]]
        self.max_use = 22
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _GDS(self,segment) -> dict:
        keys = ["nature_of_cargo"]
        child_keys = [["nature_of_cargo_coded"]]
        self.max_use = 4
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _LOC(self,segment) -> dict:
        keys = ["location_function_code_qualifier","location_identification","related_location_one_identification","related_location_two_identification"]
        child_keys = [["location_name_code","code_list_identification_code","code_list_responsible_agency_code","location_name"],["related_place/location_one_identification","code_list_identification_code","code_list_responsible_agency_code","related_place/location_one"]]
        self.max_use = 1
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _DTM(self,segment) -> dict:
        self.max_use = 3
        result = {}
        keys = ["date_time_period"]
        child_keys = [["date_time_period_function_code_qualifier","date_time_period_value","date_time_period_format_code"]]
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _RFF(self,segment) -> dict:
        keys = ["reference"]
        child_keys = [["reference_function_code_qualifier","reference_identifier"]]
        self.max_use = 3
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result

    def _TDT(self,segment) -> dict:
        keys = ["transport_stage_code_qualifier","conveyance_reference_number","mode_of_transport","transport_means","carrier","transit_direction_indicator_code","excess_transportation_information","transport_identification"]
        child_keys = [["transport_mode_name_code"],["transport_means_description_code","transport_means_description"],["carrier_identification","code_list_identification_code","code_list_responsible_agency_code"],["transport_means_identification_name_identifier","code_list_responsible_agency_code","transport_menas_identification_name","nationality_of_means_of_transport_coded"]]
        self.max_use = 2
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result

    def _NAD(self,segment) -> dict:
        keys = ["party_function_code_qualifier","party_identification_details","name_and_address","party_name","street","city_name","country_sub-entity_details","postal_identification_code","country_name_code"]
        child_keys = [["party_identifier","code_list_identification_code","code_list_responsible_agency_code"],["name_and_address_line","name_and_address_line","name_and_address_line","name_and_address_line","name_and_address_line"],["party_name","party_name","party_name","party_name","party_name","party_name_format_code"],["street_and_number/p.o._box","street_and_number/p.o._box","street_and_number/p.o._box","street_and_number/p.o._box","street_and_number/p.o._box"],["country_sub_entity_name_code","code_list_identification_code","code_list_responsible_agency_code","country_sub-entity_name"]]    
        self.max_use = 4
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _GID(self,segment) -> dict:
        keys = ["goods_item_number","number_and_type_of_packages"]
        child_keys = [["number_of_packages","package_type_description_code","code_list_identification_code","code_list_responsible_agency_code","type_of_packages"]]
        self.max_use = 4
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _MEA(self,segment) -> dict:
        keys = ["measurement_attribute_code","measurement_details","value/range"]
        child_keys = [["measured_attribute_code"],["measurement_unit_code","measurement_value"]]
        self.max_use = 4
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
        
    def _DIM(self,segment) -> dict:
        self.max_use = 4
        result = {}
        result["dimension_qualifier"] = segment[0]
        result["dimensions"]["measurement_unit_code"] = segment[1][0]
        result["dimensions"]["length_dimension"] = segment[1][1]
        result["dimensions"]["width_dimension"] = segment[1][2]
        result["dimensions"]["height_dimension"] = segment[1][3]
        return result
    
    def _DGS(self,segment) -> dict:
        self.max_use = 4
        result = {}
        result["dangerous_goods_regulations_code"] = segment[0]
        result["hazard_code"]["hazard_code_identification"] = segment[1][0]
        result["hazard_code"]["hazard_subtance_number"] = segment[1][1]
        result["hazard_code"]["hazard_code_version_number"] = segment[1][2]
        result["undg_information"]["undg_number"] = segment[2][0]
        result["dangerous_goods_shipment_flashpoint"]["shipment_flashpoint"] = segment[3][0]
        result["dangerous_goods_shipment_flashpoint"]["measurement_unit_code"] = segment[3][1]
        result["packing_group_coded"] = segment[4]
        result["ems_number"] = segment[5]
        result["trem_card_number"] = segment[6]
        result["dangerous_goods_label"]["dangerous_goods_label_marking"] = segment[7][0]
        return result
    
    def _EQD(self,segment) -> dict:
        keys = ["equipment_type_code_qualifier","equipment_identification","equipment_size_and_type","equipment_supplier,coded","equipment_status_code","full/empty_indicator,coded"]
        child_keys = [["equipment_identification_number","code_list_identification_code","code_list_responsible_agency_code","country_name_code"],["equipment_size_and_type_description_code","code_list_identification_code","code_list_responsible_agency_code","equipment_size_and_type_description"]]
        self.max_use = 4
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _EQN(self,segment) -> dict:
        keys = ["number_of_unit_details"]
        child_keys = [["number_of_units","unit_type_code_qualifier"]]
        self.max_use = 4
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _TMD(self,segment) -> dict:
        keys = ["movement_type","equipment_plan","haulage_arrangements,coded"]
        child_keys = [["movement_type_description_code"]]
        self.max_use = 4
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _HAN(self,segment) -> dict:
        result = {}
        result["handling_instructions"]["handling_instructions_coded"] = segment[0][0]
        return result
    
    def _TMP(self,segment) -> dict:
        keys = ["temperature_qualifier","temperature_setting"]
        child_keys = [["temperature_setting","measurement_unit_code"]]
        self.max_use = 4
        result = {}
        count_list_item = 0
        for i in range(0,len(segment)):
            if isinstance(segment[i],list):
                result[keys[i]] = dict(zip(child_keys[count_list_item],segment[i]))
                count_list_item += 1
            else:
                result[keys[i]] = segment[i]
        return result
    
    def _UNT(self,segment) -> dict:
        self.max_use = 4
        result = {}
        result["number_of_segments_in_a_message"] = segment[0]
        result["message_reference_number"] = segment[1]
        return result
    
    def _UNZ(self,segment) -> dict:
        self.max_use = 4
        result = {}
        result["interchange_control_count"] = segment[0]
        result["interchange_control_reference"] = segment[1]
        return result
        
    def isInSegmentGroup(self,segment):
        """Check if the message has reached the segment group or not (tag not in the first 10 segments of the message)
        """
        if self.start_segment_group:
            return True
        else:        
            self.start_segment_group =  segment.tag not in ["","UNB","UNH","BGM","CTA","COM","DTM","TSR","FTX","FTX","GDS"]
        return self.start_segment_group
    
    def findSegmentGroup(self,segment) -> list[str]:
        """Find the segment group which the segment in
            :param segment: The segment to find
            :returns: the segment group found or None
        """
        for value in self.segment_group.values():
            if segment.tag in value:
                self.current_segment_group = value
                return value
        return None
    
    def isInCurrentSegmentGroup(self,segment) -> bool:
        return segment.tag in self.current_segment_group
    
    def processSegmentGroup(self,segment_array:list,current_segment_group:list[str]):
        final_res = {}
        child_segment_group_elements = []
        final_res_item = {}
        child_segment_group = []
        key = current_segment_group[0]
        for segment in segment_array:
            # case 1: key of working segment
            if segment.tag == key:
                try:
                    func = getattr(ProcessEDI,f"_{segment.tag}")
                    segment_dict = func(self,segment.elements)
                except:
                    raise Exception("parse error")
                
                if final_res_item.get(key) is None:
                    final_res_item[key] = segment_dict
                # a segment tag's key value already exist => segment group has been repeated
                elif isinstance(final_res,list):
                    final_res.append(final_res_item)
                    final_res_item[key] = segment_dict
                else:
                    final_res = [final_res_item]
                    final_res_item[key] = segment_dict
            # case 2: key of child segment group
            elif segment.tag in self.segment_group.keys():
                if not child_segment_group:
                    child_segment_group = self.segment_group[f"{segment.tag}"]
                if segment.tag in child_segment_group:
                    child_segment_group_elements.append(segment)
                else:
                    final_res_item[child_segment_group[0]] = self.processSegmentGroup(child_segment_group_elements,child_segment_group)
                    child_segment_group = self.segment_group[f"{segment.tag}"]
                    child_segment_group_elements = [segment]
            # case 3: segment in child segment group
            elif segment.tag in child_segment_group:
                child_segment_group_elements.append(segment)
            # case 4: segment in main segment group
            else:
                try:
                    func = getattr(ProcessEDI,f"_{segment.tag}")
                    segment_dict = func(self,segment.elements)
                except:
                    raise Exception("parse error")
                final_res_item[segment.tag] = segment_dict
        if child_segment_group_elements:
            final_res_item[child_segment_group[0]] = self.processSegmentGroup(child_segment_group_elements,child_segment_group)
        if final_res_item and isinstance(final_res,list):
            final_res.append(final_res_item)
        else:
            final_res = final_res_item
        return final_res
    
    def processSegments(self,segment_array:list):
        for segment in segment_array:
            if self.isInSegmentGroup(segment):
                if self.isInCurrentSegmentGroup(segment):
                    self.current_segment_group_elements.append(segment)
                else:
                    if self.current_segment_group:
                        self.final_res[self.current_segment_group[0]] = self.processSegmentGroup(self.current_segment_group_elements,self.current_segment_group)
                    self.current_segment_group_elements = [segment]
                    self.current_segment_group = self.findSegmentGroup(segment)
            else:
                try :
                    func = getattr(ProcessEDI,f"_{segment.tag}")
                    segment_dict = func(self,segment.elements)
                    self.addDictToFinalJson(segment.tag,segment_dict)
                    print("=============================================")
                    print(json.dumps(self.final_res,indent=2))
                except:
                    raise Exception("parse error")
              
            
        return self.final_res
            
                        
                
    def checkRepeat(self,segment,max_use):
        if self.current_tag == segment.tag:
            self.count_repeat +=1
        else:
            self.count_repeat = 1
        if(self.count_repeat > max_use):
            raise Exception(f"Maximum repeat on segment {segment.tag}")
    
    
    def addDictToFinalJson(self,tag,segment_dict):
        # if final_res already having a segment with the same tag with the current processing segment, add to list
        if self.count_repeat > 1: 
            if not isinstance(self.final_res[tag],list):
                self.final_res[tag] = [segment_dict, self.current_dict]
            else:
                self.final_res[tag].append(segment_dict)
        else:
            self.final_res[tag] = segment_dict
        self.current_dict = segment_dict
        self.current_tag = tag
        
    
        
    