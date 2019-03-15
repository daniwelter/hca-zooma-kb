from argparse import ArgumentParser
import requests, pprint



all_mappings = {}

INGEST_API_URL = 'http://api.ingest.data.humancellatlas.org/submissionEnvelopes/'

pp = pprint.PrettyPrinter(indent=4)

def extract_mappings(envelope_id, file):
    jsonRaw = requests.get(INGEST_API_URL + envelope_id).json()

    projects_link = jsonRaw['_links']['projects']['href']

    project_json = requests.get(projects_link).json()
    project_content = project_json['_embedded']['projects'][0]['content']

    project_name = project_content['project_core']['project_short_name']

    biomaterials_link = jsonRaw['_links']['biomaterials']['href']
    process_json(biomaterials_link, 'biomaterials', file, project_name)

    protocols_link = jsonRaw['_links']['protocols']['href']
    process_json(protocols_link, 'protocols', file, project_name)



def process_json(link, type, file, project_name):
    done = False
    while not done:
        entries = requests.get(link).json()

        for entry in entries['_embedded'][type]:
            read_properties(entry['content'], file, project_name)

        if 'next' in entries['_links']:
            link = entries['_links']['next']['href']
        else:
            done = True



def read_properties(data, file, project_name, root=None):
    for k, v in data.items():
        if isinstance(v, dict):
            if "ontology" in v:
                ontology = v['ontology'].strip()
                text = v['text'].strip()

                print(project_name + "\t" + k + "\t" + text + "\t" + ontology)
                file.write(project_name + "\t" + k + "\t" + text + "\t" + ontology + "\n")

            else:
                read_properties(v, file, project_name, k)

        elif isinstance(v, list):
            for index, e in enumerate(v):
                if isinstance(e, dict):
                    if "ontology" in e.keys():
                        ontology = e['ontology'].strip()
                        text = e['text'].strip()

                        print(project_name + "\t" + k + "\t" + text + "\t" + ontology)
                        file.write(project_name + "\t" + k + "\t" + text + "\t" + ontology + "\n")

                    else:
                        read_properties(e, file, project_name, k)


if __name__ == '__main__':
    # parser = ArgumentParser()
    # parser.add_argument("-s", "--s", dest="submission_envelopes", action="append",
    #                   help="Submission envelope ID for submissions to process")
    #
    # args = parser.parse_args()
    #
    # envelope_ids = []
    #
    # if args.submission_envelopes:
    #     for se in args.submission_envelopes:
    #         envelope_ids.append(se)
    # else:
    #     print("You have to provide a JSON document to migrate")
    #     exit(2)

    envelope_ids = ['5c2dfb101603f500078b28de',
                '5bdc209b9460a300074b7e67',
                '5c07e2029460a300075019b1',
                '5c06cf339460a30007501909',
                '5bf53a6a9460a300074dc824',
                '5c48410e1603f500078b4c3a',
                '5bffae409460a300074f3815',
                '5c054a529460a300074f5007',
                '5be1bede9460a300074d1fe2',
                '5c055aca9460a300074f87da',
                '5bfe4d3a9460a300074eebc8',
                '5c06c6ad9460a300074fc27f',
                '5c06a9cf9460a300074fc183',
                '5c06ccdc9460a300074fc2a7',
                '5c06c34f9460a300074fc246',
                '5c51805d5fc0000007998f72'
                    ]
    file = open("all_mappings.text", "w")
    file.write("STUDY\tPROPERTY_TYPE\tPROPERTY_VALUE\tSEMANTIC_TAG\n")

    for eid in envelope_ids:
        print("Processing " + eid)
        extract_mappings(eid, file)

    file.close()

    # pp.pprint(all_mappings)

