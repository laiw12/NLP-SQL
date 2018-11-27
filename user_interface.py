from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__, static_url_path='/static')
from NodeMapper import NodeMapper
from SQLgenerator import SQLgenerator



@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/node_mapping', methods=['POST'])
def node_mapping():
    # TODO
    # dummy results
    NL_query = request.form['NL_query']
    val_type_sql_node_only = NodeMapper.get_final_map(NL_query)

    mapping_results = []
    for val_type_sql in val_type_sql_node_only:
        result = {}
        result["node_val"] = val_type_sql[0]
        result["node_type"] = val_type_sql[1]
        result["node_sql"] = val_type_sql[2]
        mapping_results.append(result)

    displays = NodeMapper.preserve_orginal_order_mapping2(NL_query, val_type_sql_node_only)

    return render_template('mapping_result.html', mapping_results=mapping_results, displays=displays, NL_query=NL_query)

@app.route('/remapping', methods=['POST'])
def remapping():
    NL_query = request.form["NL_query"]
    print(NL_query)
    mapping_after_edit = list(zip(request.form.getlist("node_val"), request.form.getlist("node_type"), request.form.getlist("node_sql")))

    mapping_results = []
    for val_type_sql in mapping_after_edit:
        result = {}
        result["node_val"] = val_type_sql[0]
        result["node_type"] = val_type_sql[1]
        result["node_sql"] = val_type_sql[2]
        mapping_results.append(result)

    displays = NodeMapper.preserve_orginal_order_mapping2(NL_query, mapping_after_edit)
    return render_template('mapping_result.html', mapping_results=mapping_results, displays=displays, NL_query=NL_query)

@app.route('/display', methods=['POST'])
def dispaly():
    # print(request.form.getlist("node_val"))
    # print(request.form.getlist("node_type"))
    NL_query = request.form["NL_query"]
    mapping_results = list(zip(request.form.getlist("node_val"), request.form.getlist("node_type"), request.form.getlist("node_sql")))
    # generate sql
    sql = SQLgenerator.generate_final_sql(NL_query, mapping_results)
    return render_template('final_sql.html', res_sql=sql)





# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()