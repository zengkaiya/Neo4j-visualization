import json
import requests
from django.shortcuts import render

# 连接数据库
NEO4J_URL = 'http://localhost:7474/db/n10s/tx/commit'
NEO4J_AUTH = ('neo4j', '20090526Rui')


# 定义一个函数发送 Cypher 查询请求
def run_cypher_query(query):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"statements": [{"statement": query}]})
    response = requests.post(NEO4J_URL, data=data, headers=headers, auth=NEO4J_AUTH)
    return response.json()


# 查询所有节点和关系
def search_all():
    return 0
    data = []
    links = []

    # 查询所有节点
    query = "MATCH (n) RETURN n"
    result = run_cypher_query(query)

    for record in result['results'][0]['data']:
        node = record['row'][0]
        node_name = node.get('name', 'Unknown')
        node_dict = {
            'name': node_name,
            'symbolSize': 50,
            'category': '对象'
        }
        data.append(node_dict)

    # 查询所有关系
    query = "MATCH (n)-[r]->(m) RETURN n, r, m"
    result = run_cypher_query(query)

    for record in result['results'][0]['data']:
        source = record['row'][0].get('name', 'Unknown')
        target = record['row'][2].get('name', 'Unknown')
        relationship_type = record['row'][1].get('type', 'UNKNOWN_REL')
        link_dict = {
            'source': source,
            'target': target,
            'name': relationship_type
        }
        links.append(link_dict)

    # 将节点和关系数据封装为字典
    neo4j_data = {
        'data': data,
        'links': links
    }

    return json.dumps(neo4j_data)


# 查询特定节点及其相关的节点和关系
def search_one(value):
    data = []
    links = []

    # 查询指定节点是否存在
    query = f"MATCH (n) RETURN n"
    result = run_cypher_query(query)
    # print(111)
    # 找个里面的逻辑还得改，怎么查询节点
    if result['results'][0]['data']:
        # 如果节点存在，将该节点加入 data 数组
        node_dict = {
            'name': value,
            'symbolSize': 50,
            'category': '对象'
        }
        data.append(node_dict)

        # 查询该节点的相关节点和关系
        query = f"""
        MATCH (n:person {{name: '{value}'}})-[rel]-(m:person)
        RETURN n, rel, m
        """
        result = run_cypher_query(query)

        for record in result['results'][0]['data']:
            target = record['row'][2].get('name', 'Unknown')
            relationship_type = record['row'][1].get('type', 'UNKNOWN_REL')

            # 添加相关节点
            target_dict = {
                'name': target,
                'symbolSize': 50,
                'category': '对象'
            }
            data.append(target_dict)

            # 添加关系
            link_dict = {
                'source': value,
                'target': target,
                'name': relationship_type
            }
            links.append(link_dict)

        search_neo4j_data = {
            'data': data,
            'links': links
        }
        return json.dumps(search_neo4j_data)
    else:
        return 0


# 视图函数
def index(request):
    ctx = {}
    if request.method == 'POST':
        node_name = request.POST.get('node')
        search_neo4j_data = search_one(node_name)
        print(node_name)
        print(search_neo4j_data)
        search_neo4j_data = [
            {
                'data': [
                    {'name': 'SearchNode1', 'category': 0, 'des': 'This is SearchNode 1'},
                    {'name': 'SearchNode2', 'category': 1, 'des': 'This is SearchNode 2'},
                ],
                'links': [
                    {'source': 'SearchNode1', 'target': 'SearchNode2', 'name': 'SearchRelation'},
                ]
            }
        ]
        if search_neo4j_data == 0:
            print(-1)
            ctx = {'title': '数据库中暂未添加该实体'}
            neo4j_data = search_all()
            return render(request, 'index.html', {'neo4j_data': neo4j_data, 'ctx': ctx})
        else:
            # 走的是这里
            neo4j_data = search_all()
            print(2)
            neo4j_data = [
                {
                    'data': [
                        {'name': 'Node1', 'category': 0, 'des': 'This is Node 1'},
                        {'name': 'Node2', 'category': 1, 'des': 'This is Node 2'},
                        {'name': 'Node3', 'category': 2, 'des': 'This is Node 3'},
                    ],
                    'links': [
                        {'source': 'Node1', 'target': 'Node2', 'name': 'Relation1'},
                        {'source': 'Node2', 'target': 'Node3', 'name': 'Relation2'},
                    ]
                }
            ]
            neo4j_data = search_neo4j_data
            ctx = None
            return render(request, 'index.html',
                          {'neo4j_data': json.dumps(neo4j_data),
                           'search_neo4j_data': json.dumps(search_neo4j_data),
                           'ctx': ctx})

    neo4j_data = search_all()
    # print(neo4j_data)
    return render(request, 'index.html', {'neo4j_data': neo4j_data, 'ctx': ctx})