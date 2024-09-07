
from Database import *
from neomodel import config





# 查询特定疾病
disease = Disease.nodes.get(disease_id="MESH:C538288",)
print(disease)