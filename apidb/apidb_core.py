from flask import jsonify, request




# Generic part
def rename_function(new_name):
    def decorator(f):
        f.__name__ = new_name
        return f
    return decorator



def initialize_fastapi(app,db_api_dict,column_names,mysql):
    """
    Example: 
        db_api_dict={'users':'read','items':['read','create']}
        column_names=["username","age"]
    
    """
    for k,v in db_api_dict.items():
        if 'read' in v:
            @app.get("/api/"+k)
            @rename_function('read_all_'+k)
            def read_all_x(k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM "+k)
                rv = cur.fetchall()
                return jsonify(rv)
    
        if 'create' in v:
            item=k[:-1]
            @app.post("/api/"+k)
            @rename_function('create_'+item)
            def add_item(k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                #column1 = request.get_json()[column_names[0]]
                columns=[request.get_json(force=True)[column_name] for column_name in column_names]
                print("COLUMNS",columns)
                #column2 = request.get_json()[column_names[1]]
                columns_str=[str(x) for x in columns]
                print("INSERT INTO "+k+" ("+",".join(column_names)+") VALUES ('" + "','".join(columns_str) + "')")
                cur.execute("INSERT INTO "+k+" ("+",".join(column_names)+") VALUES ('" + "','".join(columns_str) + "')")
                            #,"+column_names[1]+"
                            #'"+str(column2)+"'
         
                mysql.connection.commit()                
                result = {column_names[i]:columns[i] for i in range(len(column_names))}          
                return jsonify({"result": result})
    
        if 'update' in v:
            item=k[:-1]
            @app.put("/api/"+k+"/<id>")
            @rename_function('update_'+item)
            def update_item(id,k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                column1 = request.get_json()[column_names[0]]
                
                cur.execute("UPDATE "+k+" SET "+column_names[0]+" = '" + str(column1) + "' where id = " + id)
                mysql.connection.commit()
                result = {column_names[0]:column1}
            
                return jsonify({"reuslt": result})
    
        if 'delete' in v:
            item=k[:-1]
            @app.delete("/api/"+k+"/<id>")
            @rename_function('delete_'+item)
            def delete_item(id,k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                response = cur.execute("DELETE FROM "+k+" where id = " + id)
                mysql.connection.commit()
            
                if response > 0:
                    result = {'message' : 'record deleted'}
                else:
                    result = {'message' : 'no record found'}
                return jsonify({"result": result})



def initialize_flask_api(app,db_api_dict,column_names,mysql):
    """
    Example: 
        db_api_dict={'users':'read','items':['read','create']}
        column_names=["username","age"]
    
    """
    for k,v in db_api_dict.items():
        if 'read' in v:
            @app.route('/api/'+k, methods=['GET'])
            @rename_function('read_all_'+k)
            def read_all_x(k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM "+k)
                rv = cur.fetchall()
                return jsonify(rv)
    
        if 'create' in v:
            item=k[:-1]
            @app.route('/api/'+item, methods=['POST'])
            @rename_function('create_'+item)
            def add_item(k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                #column1 = request.get_json()[column_names[0]]
                columns=[request.get_json(force=True)[column_name] for column_name in column_names]
                print("COLUMNS",columns)
                #column2 = request.get_json()[column_names[1]]
                columns_str=[str(x) for x in columns]
                print("INSERT INTO "+k+" ("+",".join(column_names)+") VALUES ('" + "','".join(columns_str) + "')")
                cur.execute("INSERT INTO "+k+" ("+",".join(column_names)+") VALUES ('" + "','".join(columns_str) + "')")
                            #,"+column_names[1]+"
                            #'"+str(column2)+"'
         
                mysql.connection.commit()                
                result = {column_names[i]:columns[i] for i in range(len(column_names))}          
                return jsonify({"result": result})
    
        if 'update' in v:
            item=k[:-1]
            @app.route("/api/"+item+"/<id>", methods=['PUT'])
            @rename_function('update_'+item)
            def update_item(id,k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                column1 = request.get_json()[column_names[0]]
                
                cur.execute("UPDATE "+k+" SET "+column_names[0]+" = '" + str(column1) + "' where id = " + id)
                mysql.connection.commit()
                result = {column_names[0]:column1}
            
                return jsonify({"reuslt": result})
    
        if 'delete' in v:
            item=k[:-1]
            @app.route("/api/"+item+"/<id>", methods=['DELETE'])
            @rename_function('delete_'+item)
            def delete_item(id,k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                response = cur.execute("DELETE FROM "+k+" where id = " + id)
                mysql.connection.commit()
            
                if response > 0:
                    result = {'message' : 'record deleted'}
                else:
                    result = {'message' : 'no record found'}
                return jsonify({"result": result})
