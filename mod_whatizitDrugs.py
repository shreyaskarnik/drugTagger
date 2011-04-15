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
        ("'", '&#39;'))

    for rep, orig in htmlCodes:
        kinda_xml = kinda_xml.replace(orig, rep)
    return kinda_xml



def generate_whatizit_client():
    """Generates a SUDS client for the Whatizit webservice."""

    url = 'http://www.ebi.ac.uk/webservices/whatizit/ws?wsdl'
    client = Client(url, faults = False, retxml = False)
    return client
    


def ask_whatizit(raw_text, client = None, pipeline = 'whatizitEBIMed'):
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
        
        return (de_safe_xml(response),tagged_text)
    


def run_batch (in_path,out_path):
    for infile in glob.glob( os.path.join(in_path, '*.txt') ):
        fname=os.path.basename(infile)
        real_name=os.path.splitext(fname)[0]
        text_in=open(infile, 'r+')
        text_raw=text_in.read()
        text_in.close()
        (resp,tagged_text)=ask_whatizit(text_raw)
        if(resp==200):
            out_xml_name=real_name+'.xml'
            out_file=os.path.join(out_path,out_xml_name)
            text_out=open(out_file,'w')
            text_out.write(tagged_text)
            text_out.close()
        else:
            print "Error in file: " + infile
        
