# -*- coding: utf8 -*-
from suds.client import Client
import re
import os
import glob
### Thanks to JudoWill (Will Dampier) for the help regarding this code.



def de_safe_xml(kinda_xml):
    """Converts an escaped HTML/XML into a more normal string."""

    htmlCodes = (
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('"', '&quot;'),
        ("'", '&#39;'),
        ("\'", '&#39;'))

    for rep, orig in htmlCodes:
        kinda_xml = kinda_xml.replace(orig, rep)
    return kinda_xml



def generate_whatizit_client():
    """Generates a SUDS client for the Whatizit webservice."""

    url = 'http://www.ebi.ac.uk/webservices/whatizit/ws?wsdl'
    client = Client(url, faults = False)
    return client
    


def ask_whatizit(raw_text, client = None, pipeline = 'whatizitDrugs'):
    """A function which queries the Whatizit tool use the SOAP client.

Care is taken to ensure that identical sentences are not querried
multiple times.

Arguments:
search_sent_list -- A LIST of sentences to search.
client = None -- A SOAP client ... If None then one is created on the fly.
pipeline = 'whatizitSwissprot' -- The pipeline to search.
"""

    if client is None:
        client = generate_whatizit_client()
        (response,tagged_text) = client.service.contact(pipelineName = pipeline,
                                        text = raw_text,
                                        convertToHtml = False)
        
        return (response,de_safe_xml(tagged_text))
    

def ask_whatizit_pmid(pid, client = None, pipeline = 'whatizitDrugs'):
   
    if client is None:
        client = generate_whatizit_client()
        (response,fetched_abst) = client.service.queryPmid(pipelineName = pipeline,
                                        pmid = pid)
        
        return (response,de_safe_xml(fetched_abst))




def run_batch (in_path,out_path):
    for infile in glob.glob( os.path.join(in_path, '*.txt') ):
        fname=os.path.basename(infile)
        real_name=os.path.splitext(fname)[0]
        with open(infile, 'r+') as text_in:
            text_raw=text_in.read()
    
        (resp,tagged_text)=ask_whatizit(de_safe_xml(text_raw))
        if(resp==200):
            out_xml_name=real_name+'.html'
            out_file=os.path.join(out_path,out_xml_name)
            with open(out_file,'w') as text_out:
                text_out.write(tagged_text)
        else:
            print "Error in file: " + infile
