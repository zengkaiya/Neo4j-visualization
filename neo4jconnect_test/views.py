import json
import requests
from django.shortcuts import render
from .func import *


# 查询所有节点和关系





last_request = None

# 视图函数
def index(request):
    ctx = {}
    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'search':
            node_or_edge = request.POST.get('node_or_edge')
            property_name = request.POST.get('property_name')
            property_value = request.POST.get('property_value')


            che_id_ans = model.find_chemical_by_id(property_value)
            dis_id_ans = model.find_disease_by_id(property_value)
            che_name_ans = model.find_chemical_by_name(property_value)
            dis_name_ans = model.find_disease_by_name(property_value)

            if che_id_ans == None and che_name_ans == None and dis_id_ans == None and dis_name_ans == None:
                ctx = {'title': '数据库中暂未添加该实体'}
                return render(request, 'index.html', {'neo4j_data': neo4j_data, 'ctx': ctx})
            
            elif che_id_ans != None or che_name_ans != None:
                links_ans = model.find_diseases_associated_with_chemical(property_value)
            elif dis_id_ans != None or dis_name_ans != None:
                links_ans = model.find_chemicals_associated_with_disease(property_value)
            else:
                links_ans = []
            
            search_data = [
            {
                'data': [
                    {'name': 'SearchNode1', 'category': 0, 'des': 'This is SearchNode 1'},
                ],
                'links': [
                    {'source': 'SearchNode1', 'target': 'SearchNode2', 'name': 'SearchRelation'},
                ]
            }
        ]



            
            print(f'node/edge: {node_or_edge}, property_name: {property_name}, property_value: {property_value}')

            pass

        elif action == 'add':
            pass

        elif action == 'delete':
            pass

        elif action == 'update':
            pass

        node_or_edge = request.POST.get('node_or_edge')
        property_name = request.POST.get('property_name')
        property_value = request.POST.get('property_value')

        print(f'node/edge: {node_or_edge}, property_name: {property_name}, property_value: {property_value}')

        if node_or_edge == 'node':
            if property_name != '':
                search_neo4j_data = model.search_node_by_property(property_name, property_value)

            elif property_name == '':
                search_neo4j_node_d = model.find_disease_by_name
                search_neo4j_data = model.search_node_by_name(property_value)

        elif node_or_edge == 'edge':
            pass

        else:
            return render(request, 'index.html', {'ctx': ctx})


        
    #     search_neo4j_data = [
    #         {
    #             'data': [
    #                 {'name': 'SearchNode1', 'category': 0, 'des': 'This is SearchNode 1'},
    #                 {'name': 'SearchNode2', 'category': 1, 'des': 'This is SearchNode 2'},
    #             ],
    #             'links': [
    #                 {'source': 'SearchNode1', 'target': 'SearchNode2', 'name': 'SearchRelation'},
    #             ]
    #         }
    #     ]
    #     if search_neo4j_data == 0:
    #         print(-1)
    #         ctx = {'title': '数据库中暂未添加该实体'}
    #         neo4j_data = search_all()
    #         return render(request, 'index.html', {'neo4j_data': neo4j_data, 'ctx': ctx})
    #     else:
    #         # 走的是这里
    #         neo4j_data = search_all()
    #         print(2)
    #         neo4j_data = [
    #             {
    #                 'data': [
    #                     {'name': 'Node1', 'category': 0, 'des': 'This is Node 1'},
    #                     {'name': 'Node2', 'category': 1, 'des': 'This is Node 2'},
    #                     {'name': 'Node3', 'category': 2, 'des': 'This is Node 3'},
    #                 ],
    #                 'links': [
    #                     {'source': 'Node1', 'target': 'Node2', 'name': 'Relation1'},
    #                     {'source': 'Node2', 'target': 'Node3', 'name': 'Relation2'},
    #                 ]
    #             }
    #         ]
    #         neo4j_data = search_neo4j_data
    #         ctx = None
    #         return render(request, 'index.html',
    #                       {'neo4j_data': json.dumps(neo4j_data),
    #                        'search_neo4j_data': json.dumps(search_neo4j_data),
    #                        'ctx': ctx})

    neo4j_data = []
    
    return render(request, 'index.html', {'neo4j_data': neo4j_data, 'ctx': ctx})