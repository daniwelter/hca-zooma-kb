# hca-zooma-kb
Script to extract all existing ontology annotations in HCA Ingest for a given set of submissions.

The script takes a list of submission envelope IDs and extracts the corresponding ontology annotations from the ingest API (prod). The envelope IDs are currently hard-coded but the script also has a commented-out section that allows it to take a list of IDs as an input parameter. 

The script generates a file called all_mappings.txt, which contains every single free-text to ontology term mapping in every biomaterial or process in every submission requested. To get a list of unique mappings by project, run:

`sort all_mappings.text | uniq > all_mappings_unique.txt`

