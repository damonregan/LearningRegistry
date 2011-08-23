'''
Created on Aug 16, 2011

@author: jklo
'''
from services import ServiceTemplate
from setup_utils import getInput, PublishDoc, isBoolean, YES, isInt
import pystache, uuid
import json


def install(server, dbname, setupInfo):
    custom_opts = {}
    active = getInput("Enable Basic Harvest?", "T", isBoolean)
    custom_opts["active"] = active.lower() in YES
    
    active = getInput("Enable Basic Harvest Flow Control?", "F", isBoolean)
    custom_opts["flow_control"] = active.lower() in YES
    
#    if custom_opts["flow_control"]:
#        active = getInput("Maximum IDs to Return?", "100", isInt)
#        custom_opts["id_limit"] = int(active)
#        active = getInput("Maximum Docs to Return?", "100", isInt)
#        custom_opts["doc_limit"] = int(active)
        
        
    custom_opts["node_endpoint"] = setupInfo["nodeUrl"]
    custom_opts["service_id"] = uuid.uuid4().hex
    
    must = __BasicHarvestServiceTemplate()
    config_doc = must.render(**custom_opts)
    doc = json.loads(config_doc)
    PublishDoc(server, dbname, "Basic Harvest service", doc)
    print("Configured Basic Harvest service:\n{0}\n".format(json.dumps(doc, indent=4, sort_keys=True)))




class __BasicHarvestServiceTemplate(ServiceTemplate):
    service_data_template = '''{
        "granularity": "YYYY-MM-DDThh:mm:ssZ",
        "setSpec": null{{#spec_kv_only}},
        "spec_kv_only": {{spec_kv_only}}{{/spec_kv_only}},
        "flow_control": {{flow_control}}{{#id_limit}},
        "id_limit": {{id_limit}}{{/id_limit}}{{#doc_limit}},
        "doc_limit": {{doc_limit}}{{/doc_limit}},
        "metadataformats": [
            {
                "metadataFormat": "LR Resource Data Description Data Model",
                "metadataPrefix": "LR_JSON_0.10.0"
            }
        ]
    }'''
    
    
    
    def _optsoverride(self):
        opts = {
            "active": "false",
            "service_name": "Basic Harvest",
            "service_version": "0.10.0",
            "service_endpoint": None,
            "service_key": "false", 
            "service_https": "false",
            "spec_kv_only": None,
            "flow_control": False
            
        }
        return opts
        
if __name__ == "__main__":
    import couchdb
    
    nodeSetup = {
                 'couchDBUrl': "http://localhost:5984",
                 'node_service_endpoint_url': "http://test.example.com"
    }
    
    server =  couchdb.Server(url= nodeSetup['couchDBUrl'])
    install(server, "node", nodeSetup)
    