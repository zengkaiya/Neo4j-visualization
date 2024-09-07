import requests
import json

url = "http://localhost:7474/db/n10s/tx/commit"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
data = {
    "statements": [
        {
            "statement": "MATCH (n) RETURN n LIMIT 1"
        }
    ]
}

try:
    response = requests.post(url, headers=headers, auth=("neo4j", "zxcvbnm106"), json=data)
    # 输出原始响应内容
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content.decode("utf-8"))

    # 尝试将响应内容解析为 JSON
    json_data = response.json()
    print(json.dumps(json_data, indent=4))

except Exception as e:
    print(f"Error: {e}")