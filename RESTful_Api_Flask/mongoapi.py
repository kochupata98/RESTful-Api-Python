from flask import Flask, jsonify,request
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient(u"mongodb://localhost:27017")        
mydb = myclient["MongoDb"] 
coll_name='framework'    
mycol = mydb[coll_name]

# Get all documents from mongo collection

@app.route("/")
def hello():
    return "Hello!"

@app.route('/framework', methods=['GET'])
def get_all_frameworks():
    output = []

    for q in mycol.find():
        output.append({'name' : q['name'], 'language' : q['language']})

    return jsonify({'result' : output})
    
@app.route('/framework/<name>', methods=['GET'])
def get_one_frameworks(name):
    output = []

    q = mycol.find_one({'name' : name})
    print(q)

    if q:
        output = {'name' : q['name'], 'language' : q['language']}
    else:
        output = 'No results found'

    return jsonify({'result' : output})

@app.route('/framework', methods=['POST'])
def add_framework():
    #framework = mongo.db.framework 

    name = request.json['name']
    language = request.json['language']

    framework_id = mycol.insert({'name' : name, 
                                     'language' : language})
    new_framework = mycol.find_one({'_id' : framework_id})

    output = {'name' : new_framework['name'], 'language' : new_framework['language']}

    return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True)