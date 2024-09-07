
import json
with open('./config.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)
    print(json_data)
    database = json_data['database']
    password = json_data['password']

from neomodel import db
from neomodel import StructuredNode, StringProperty, FloatProperty, RelationshipTo, RelationshipFrom
from neomodel import config

# Using config option
config.DATABASE_URL = f'bolt://{database}:{password}@localhost:7687'


# 定义 Disease 模型
class Disease(StructuredNode):
    name = StringProperty(required=True)
    disease_id = StringProperty(unique_index=True)
    alt_ids = StringProperty()
    definition = StringProperty()

# 定义 Chemical 模型
class Chemical(StructuredNode):
    name = StringProperty(required=True)
    chemical_id = StringProperty(unique_index=True)
    cas_rn = StringProperty()
    definition = StringProperty()
    
    # 定义与 Disease 的关系
    associated_with = RelationshipTo('Disease', 'ASSOCIATED_WITH')

# 定义关联关系
class AssociatedWith(StructuredNode):
    direct_evidence = StringProperty()
    inference_gene_symbol = StringProperty()
    inference_score = FloatProperty()
    omim_ids = StringProperty()
    pubmed_ids = StringProperty()