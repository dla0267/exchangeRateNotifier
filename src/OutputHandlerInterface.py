import json
import requests

class ParserMeta(type):
    """A Parser metaclass that will be used for parser class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text))

"""
This interface is used for concrete classes to inherit from 
for the purpose of providing flexible options to output source data.
There is no need to define the ParserMeta methods as any class
as they are implicitly made available via .__subclasscheck__().
"""
class OutputHandlerInterface(metaclass=ParserMeta):
    def output_source_data(self, source: str):
        pass

class DiscordMessageOutputHandler(OutputHandlerInterface):

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def output_source_data(self, source: str):
        return requests.post(self.webhook_url, data=json.dumps({"content": source}),
                             headers={'Content-Type': 'application/json', })

