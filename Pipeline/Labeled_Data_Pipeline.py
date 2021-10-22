import pandas as pd
import yaml
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)


directory = os.path.normpath('../Data/APP-350_v1.1/APP-350_v1.1/annotations')

policy_list = os.listdir(directory)

raw_data = []

for file in policy_list:
    path = os.path.join(directory, file)
    with open (path) as f:
        record = yaml.safe_load(f)

    policy_id = record['policy_id']
    policy_name = record ['policy_name']
    contains_synthetic = record['contains_synthetic']

    for segment in record['segments']:
        segment.update({
            'policy_id': policy_id,
            'policy_name': policy_name,
            'contains_synthetic': contains_synthetic, })
        raw_data.append(segment)


with open(os.path.normpath('../Data/APP-350_v1.1/APP-350_v1.1/features.yml'))as f:
    features = yaml.safe_load(f)

tags = []
for i in features['data_types']:
    for p in i['practices']:
        tags.append(p)


APP_350 = pd.DataFrame(raw_data)

def parse_annotations(annotation, tag):
    """
    Funcion for parsing APP_350 annotations into binary response
    :param annotation: List of dicts containing 'practice' and 'modality' annotations
    :param tag: str. the tag being searched for
    :return: bool - does the annotation contain the given tag
    """
    practice_performed = False
    for n in annotation:
        if n['practice'] == tag and n['modality'] == 'PERFORMED':
            practice_performed = True

    return practice_performed



for tag in tags:
    col_name = 'y_' + tag
    APP_350[col_name] = APP_350['annotations'].apply(parse_annotations, args=[tag])


categories = ['3RD',
              'LOCATION',
              'DEMOGRAPHIC',
              'CONTACT',
              'IDENTIFIER',
              'SSO',
              ]

targets = [i for i in APP_350.columns if 'y_' in i]

for cat in categories:
    cols = [i for i in targets if cat in i.upper()]
    APP_350[cat] = APP_350[cols].any(axis = 1, bool_only=True)

rel_cols = ['policy_id','policy_name','segment_id', 'segment_text', *categories]

cleaned_data = APP_350[rel_cols]

save_path = os.path.normpath('../Data/Labeled_Data.csv')
if not os.path.exists(save_path):
    cleaned_data.to_csv(save_path)
