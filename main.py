from flask import Flask
import pyodbc
import json

def connect_to_db():
    # Define the connection details
    server = 'mloops.database.windows.net'
    database = 'mloops'
    username = 'readonlyuser'
    password = 'pwMloops2'
    driver = '{ODBC Driver 17 for SQL Server}'  # Make sure to use the correct driver version

    # Establish the connection
    cnxn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return cnxn


def get_models():
    cnxn = connect_to_db()
    cursor = cnxn.cursor()
    cursor.execute('SELECT ModelId, modelName FROM models')
    rows = cursor.fetchall()
    modified_rows = []
    for row in rows:
        row_to_list = [elem for elem in row]
        modified_rows.append(row_to_list)
    return json.dumps(modified_rows)

def get_recommendations(model_id):
    cnxn = connect_to_db()
    cursor = cnxn.cursor()
    cursor.execute("""select re.recommendationName, re.recommendationFunc, i.insightname, r.Score, r.threshold, i.InsightShowfunc, i.Insightfunc, r.IsNum
                                from Rules as r
                                join Insight as i on r.Insightid=i.Insightid
                                join Recommendation as re on  re.RecommendationId=r.RecommendationId
                                where r.modelId=""" + str(model_id) + " order by r.Score desc")
    rows = cursor.fetchall()
    modified_rows = []
    for row in rows:
        row_to_list = [elem for elem in row]
        modified_rows.append(row_to_list)
    return json.dumps(modified_rows)


app = Flask(__name__)

@app.route('/models/', methods=['GET'])
def models():
    return get_models()

@app.route('/recommendations/<model_id>', methods=['GET'])
def recommendations(model_id):
    return get_recommendations(model_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)