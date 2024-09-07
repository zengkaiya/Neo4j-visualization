import json
from django.shortcuts import render
from neo4j import GraphDatabase

# 连接数据库
NEO4J_BOLT_URL = "bolt://localhost:7687"  # 使用Bolt协议
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "3022244244"

# 创建Neo4j驱动器
driver = GraphDatabase.driver(NEO4J_BOLT_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 定义一个函数发送 Cypher 查询请求
def run_cypher_query(query):
    try:
        with driver.session() as session:
            result = session.run(query)
            return result.data()  # 返回查询结果
    except Exception as e:
        print(f"Error: {e}")
        return None


# 查询所有节点和关系
def search_all():
    data = []
    links = []

    # 查询所有节点
    query = "MATCH (n) RETURN n"
    result = run_cypher_query(query)

    if result:
        for record in result:
            node = record['n']
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

    if result:
        for record in result:
            source = record['n'].get('name', 'Unknown')
            target = record['m'].get('name', 'Unknown')
            relationship_type = type(record['r']).__name__
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
    query = f"MATCH (n {{name: '{value}'}}) RETURN n"
    result = run_cypher_query(query)

    if result and len(result) > 0:
        # 如果节点存在，将该节点加入 data 数组
        node_dict = {
            'name': value,
            'symbolSize': 50,
            'category': '对象'
        }
        data.append(node_dict)

        # 查询该节点的相关节点和关系
        query = f"""
        MATCH (n {{name: '{value}'}})-[rel]-(m)
        RETURN n, rel, m
        """
        result = run_cypher_query(query)

        if result:
            for record in result:
                target = record['m'].get('name', 'Unknown')
                relationship_type = type(record['rel']).__name__

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

        if search_neo4j_data == 0:
            ctx = {'title': '数据库中暂未添加该实体'}
            neo4j_data = search_all()
            return render(request, 'index.html', {'neo4j_data': neo4j_data, 'ctx': ctx})
        else:
            neo4j_data = search_all()
            return render(request, 'index.html',
                          {'neo4j_data': json.dumps(neo4j_data),
                           'search_neo4j_data': search_neo4j_data,
                           'ctx': ctx})

    neo4j_data = search_all()
    return render(request, 'index.html', {'neo4j_data': neo4j_data, 'ctx': ctx})
