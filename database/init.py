# import pandas as pd


# from Database import *


# # 读取 CSV 文件并导入数据
# def load_data():
#     # 导入 Diseases
#     diseases_df = pd.read_csv('database/csv/CTD_diseases.csv')
#     for index, row in diseases_df.iterrows():
#         disease = Disease(
#             name=row['DiseaseName'],
#             disease_id=row['DiseaseID'],
#             alt_ids=row['AltDiseaseIDs'].split('|') if pd.notnull(row['AltDiseaseIDs']) else [],
#             definition=row['Definition']
#         )
#         disease.save()

#     # 导入 Chemicals
#     chemicals_df = pd.read_csv('database/csv/CTD_chemicals.csv')
#     for index, row in chemicals_df.iterrows():
#         chemical = Chemical(
#             name=row['ChemicalName'],
#             chemical_id=row['ChemicalID'],
#             cas_rn=row['CasRN'],
#             definition=row['Definition']
#         )
#         chemical.save()

#     # 导入关系
#     associations_df = pd.read_csv('database/csv/chemicals_diseases_modified.csv')
#     for index, row in associations_df.iterrows():
#         chemical = Chemical.nodes.get(chemical_id=row['ChemicalID'])
#         disease = Disease.nodes.get(disease_id=row['DiseaseID'])

#         association = chemical.associated_with.connect(disease)
#         association.direct_evidence = row['DirectEvidence']
#         association.inference_gene_symbol = row['InferenceGeneSymbol']
#         association.inference_score = float(row['InferenceScore']) if pd.notnull(row['InferenceScore']) else None
#         association.omim_ids = row['OmimIDs'].split('|') if pd.notnull(row['OmimIDs']) else []
#         association.pubmed_ids = row['PubMedIDs'].split('|') if pd.notnull(row['PubMedIDs']) else []
#         association.save()

# # 运行导入函数
# load_data()
