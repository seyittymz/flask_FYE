import azure.cosmos.cosmos_client as cosmos_client
import config
from flask import Flask, jsonify

app = Flask(__name__)

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAİNER_ID = config.settings['container_id']
client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )


@app.route('/get_user_by_post_id/<post_id>', methods=['GET'])
def get_user_by_post_id(post_id):
    query = f"SELECT * FROM c WHERE ARRAY_CONTAINS(c.posts, {{'path': '\"users\", \"{post_id}\"'}}, true)"
    try:
        database = client.get_database_client(DATABASE_ID)
        container = database.get_container_client(CONTAİNER_ID)
        
        results = list(container.query_items(query, enable_cross_partition_query=True))
        
        if not results:
            return jsonify({"message": "Kullanici Bulunamadi."}), 404
        
        user = results[0]
        return jsonify(user)
    
    except Exception as e:
        return jsonify({"message": f"Hata olustu: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)