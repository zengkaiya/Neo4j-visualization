import json
import requests
from django.shortcuts import render
from .func import *

model = Model()


che_data = []
dis_data = []

# 视图函数
def index(request):
    ctx = {}
    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'search':
            node_or_edge = request.POST.get('node_or_edge')
            property_name = request.POST.get('property_name')
            property_value = request.POST.get('property_value')

            che_data = []
            dis_data = []
            links_data = []
            neo4j_search = []

            che_id_ans = model.find_chemical_by_id(property_value)
            dis_id_ans = model.find_disease_by_id(property_value)
            che_name_ans = model.find_chemical_by_name(property_value)
            dis_name_ans = model.find_disease_by_name(property_value)

            if che_id_ans == None and che_name_ans == None and dis_id_ans == None and dis_name_ans == None:
                ctx = {'title': '数据库中暂未添加该实体'}
                return render(request, 'index.html', {'ctx': ctx})
            

            elif che_id_ans != None or len(che_name_ans) != 0:

                if che_id_ans != None:
                    che_data.append(che_id_ans)
                else:
                    che_data.append(che_name_ans[0])

                che_id = che_data[0].chemical_id
                links_ans = model.find_diseases_associated_with_chemical(che_id)
                if len(links_ans) != 0:
                    for link in links_ans:
                        links_data.append({'source': che_id, 'target': link.disease_id, 'name': 'associated_with'})
                        dis_data.append(model.find_disease_by_id(link.disease_id))


            elif dis_id_ans != None or len(dis_name_ans) != 0:

                if dis_id_ans != None:
                    dis_data.append(dis_id_ans)
                else:
                    dis_data.append(dis_name_ans[0])

                dis_id = dis_data[0].disease_id
                links_ans = model.find_chemicals_associated_with_disease(dis_id)
                if len(links_ans) != 0:
                    for link in links_ans:
                        links_data.append({'source': dis_id, 'target': link.chemical_id, 'name': 'associated_with'})
                        che_data.append(model.find_chemical_by_id(link.chemical_id))

            neo4j_search_data = []

            if len(che_data) != 0:
                for che in che_data:
                    neo4j_search_data.append({'name': che.chemical_id, 'category': 0, 'des': che.name})

            if len(dis_data) != 0:
                for dis in dis_data:
                    neo4j_search_data.append({'name': dis.disease_id, 'category': 1, 'des': dis.name})

            neo4j_search = {'data': neo4j_search_data, 'links': links_data}
            neo4j_search = [neo4j_search]
            print(neo4j_search)

            ctx = None
            return render(request, 'index.html', {'neo4j_data': neo4j_search, 'ctx': ctx})



        elif action == 'add':
            pass

        elif action == 'delete':
            pass

        elif action == 'update':
            pass

    
    return render(request, 'index.html', {'ctx': ctx})