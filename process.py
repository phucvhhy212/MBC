import json


class ProcessEDI:
    def __init__(self) -> None:
        segments_group_1 = ["LOC","DTM"]
        segments_group_2 = ["RFF","DTM"]
        segments_group_4 = ["LOC","DTM"]
        segments_group_3 = ["TDT",segments_group_4]
        segments_group_7 = ["CTA","COM"]
        segments_group_6 = ["NAD","LOC",segments_group_7]
        segments_group_11 = ["MEA"]
        segments_group_9 = ["GID","FTX",segments_group_11]
        segments_group_12 = ["DIM"]
        segments_group_13 = ["RFF","DTM"]
        segments_group_16 = ["CTA","COM"]
        segments_group_17 = ["MEA"]
        segments_group_15 = ["DGS","FTX",segments_group_16,segments_group_17]
        segments_group_19 = ["NAD","DTM"]
        segments_group_18 = ["EQD","EQN","TMD","MEA","DIM","HAN","TMP","FTX","RFF",segments_group_19]
        
    def processSegment(self,keys,child_keys,segment):
        """Demonstrates triple double quotes
        docstrings and does nothing really.
        """
        segment_array = segment.elements
        count_list_item = 0
        new_dict = {}
        for value in segment_array:
            if isinstance(value,list):
                new_dict[keys[segment_array.index(value)]] = dict(zip(child_keys[count_list_item],value))
                count_list_item += 1
            else:
                new_dict[keys[segment_array.index(value)]] = value
        new_dict = {"tag": f"{segment.tag}","elements":new_dict}
        return new_dict
    
    def process_segment1(self,segment_array:list):
        final_res = {}
        final_array = []
        final_array_item = {}
        for segment in segment_array:
            if segment["tag"] == "LOC":
                if final_array_item.get("LOC") is None:
                    final_array_item["LOC"] = segment["elements"]
                # a segment tag's key value already exist => segment group has been repeated
                else:
                    final_array.append(final_array_item)
                    final_array_item = {}
                    final_array_item["LOC"] = segment["elements"]
            elif segment["tag"] == "DTM":
                if final_array_item.get("DTM") is None:
                    final_array_item["DTM"] = segment["elements"]
                else:
                    if isinstance(final_array_item["DTM"],dict):
                        final_array_item["DTM"] = [final_array_item["DTM"],segment["elements"]]
                    elif isinstance(final_array_item["DTM"],list) :
                        final_array_item["DTM"].append(segment["elements"])
        if len(final_array_item) != 0:
            final_array.append(final_array_item)
        final_res["segment_group_1"]= final_array
        return final_res
                    
                
    
    