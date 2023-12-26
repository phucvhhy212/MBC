import json
import inspect

class SyntaxIdentifier:
    def __init__(self, syntax_identifier,syntax_version_number):
        self.syntax_identifier = syntax_identifier
        self.syntax_version_number = syntax_version_number

class InterchangeSender:
    def __init__(self,sender_identification,partner_identification_code_qualifier=None,reverse_routing_address=None):
        self.sender_identification = sender_identification
        self.partner_identification_code_qualifier = partner_identification_code_qualifier
        self.reverse_routing_address = reverse_routing_address

class InterchangeRecipient:
    def __init__(self,recipient_identification,partner_identification_code_qualifier=None,routing_address=None):
        self.recipient_identification = recipient_identification
        self.partner_identification_code_qualifier = partner_identification_code_qualifier
        self.routing_address = routing_address

class DateTimePreparation:
    def __init__(self,date_of_preparation,time_of_preparation):
        self.date_of_preparation = date_of_preparation
        self.time_of_preparation = time_of_preparation
        
class RecipientsPassword:
    def __init__(self,recipients_password,recipients_password_qualifier):
        self.recipients_password = recipients_password
        self.recipients_password_qualifier = recipients_password_qualifier


# fixed code #    
date_time_preparation = DateTimePreparation(
    date_of_preparation= "070602",
    time_of_preparation= "0822"
)

interchange_recipient = InterchangeRecipient(
    recipient_identification= "RECEIVERID",
    partner_identification_code_qualifier = "ZZZ",
)

interchange_sender = InterchangeSender(
    sender_identification= "MSCU",
    partner_identification_code_qualifier = "ZZZ"
)

syntax_identifier = SyntaxIdentifier(
    syntax_identifier = "UNOC",
    syntax_version_number = "2"
)
##################

class InterchangeHeader:
    def __init__(
        self,
        syntax_identifier:SyntaxIdentifier,
        interchange_sender:InterchangeSender,
        interchange_recipient:InterchangeRecipient,
        date_time_preparation:DateTimePreparation,
        control_reference,
        recipients_password=None,
        application_ref=None,
        priority_code=None,
        acknowledgement_request=None,
        communication_agreement_id=None,
        test_indicator=None
    ):
        self.syntax_identifier = syntax_identifier
        self.interchange_sender = interchange_sender
        self.interchange_recipient = interchange_recipient
        self.date_time_preparation = date_time_preparation
        self.control_reference = control_reference
        self.recipients_password = recipients_password
        self.application_ref = application_ref
        self.priority_code = priority_code
        self.acknowledgement_request = acknowledgement_request
        self.communication_agreement_id = communication_agreement_id
        self.test_indicator = test_indicator
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            indent=4)


## test instance InterchangeHeader
        
interchange_header = InterchangeHeader(
    syntax_identifier = syntax_identifier,
    interchange_sender = interchange_sender,
    interchange_recipient = interchange_recipient,
    date_time_preparation = date_time_preparation,
    control_reference = 1,
)


print(interchange_header.toJSON())
print("split string: ")
text = "UNB+UNOC:3+MSCU:ZZZ+RECEIVERID:ZZZ+070602:0822+1'"
unb_elements = text.split("+")[1:]

constructor_info = inspect.signature(InterchangeHeader.__init__)

# Lọc ra các tham số của hàm khởi tạo (loại bỏ self)
constructor_params = [param.name for param in constructor_info.parameters.values()][1:]

print(interchange_header.toJSON())