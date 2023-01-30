from flask import jsonify, request





from fastapi import FastAPI



# description = """
# This is your API
# """

# app = FastAPI(title="Example API",
#               description=description,
#      version="1.0.0",
#      )




# Generic part
def rename_function(new_name):
    def decorator(f):
        f.__name__ = new_name
        return f
    return decorator

class CustomEndpoint:
    def __init__(self,app,name,operation,function,api_url="/api/"):
        self.app=app
        self.name=name #should be in plural
        self.operation=operation
        self.function=function
        self.api_url=api_url
      
         
    def initialize_custom_endpoint(self):
        if 'read_all' in self.operation:
            @self.app.get(self.api_url+self.name)
            @rename_function('read_all_'+self.name)
            def read_all_items():
                result=self.function() 
                return {"result":result}
        
        if 'read' in self.operation:
            item=self.name[:-1]
            @self.app.get(self.api_url+self.name[:-1]+"/<id>")
            @rename_function('read_'+item)
            def read_item():
                result=self.function() 
                return {"result":result}
    
        if 'create' in self.operation:
            item=self.name
            @self.app.post("/api/"+self.name)
            @rename_function('create_'+item)
            def add_item():
                result=self.function()
                return {"result":result}
            
        if 'update' in self.operation:
            item=self.name[:-1]
            @self.app.put("/api/"+self.name[:-1]+"/<id>")
            @rename_function('update_'+item)
            def update_item():
                result=self.function()
                return {"result":result}
            
        if 'delete' in self.operation:
            item=self.name[:-1]
            @self.app.delete("/api/"+self.name[:-1]+"/<id>")
            @rename_function('delete_'+item)
            def delete_item():
                result=self.function()
                return {"result":result}
            
        if 'delete_all' in self.operation:
            @self.app.delete("/api/"+self.name)
            @rename_function('delete_all_'+self.name)
            def delete_item():
                result=self.function()
                return {"result":result}
    
    
        # if 'update' in self.operation:
        #     item=self.name[:-1]
        #     @self.app.put("/api/"+self.name+"/<id>")
        #     @rename_function('update_'+item)
        #     def update_item(id,name=self.name): #name=self.name because of late binding - otherwise, it would assign all endpoints with the same name
        #         cur = mysql.connection.cursor()
        #         column1 = request.get_json()[column_names[0]]
                
        #         cur.execute("UPDATE "+self.name+" SET "+column_names[0]+" = '" + str(column1) + "' where id = " + id)
        #         mysql.connection.commit()
        #         result = {column_names[0]:column1}
            
        #         return jsonify({"reuslt": result})
    
        # if 'delete' in self.operation:
        #     item=self.name[:-1]
        #     @self.app.delete("/api/"+self.name+"/<id>")
        #     @rename_function('delete_'+item)
        #     def delete_item(id,name=self.name): #name=self.name because of late binding - otherwise, it would assign all endpoints with the same name
        #         cur = mysql.connection.cursor()
        #         response = cur.execute("DELETE FROM "+self.name+" where id = " + id)
        #         mysql.connection.commit()
            
        #         if response > 0:
        #             result = {'message' : 'record deleted'}
        #         else:
        #             result = {'message' : 'no record found'}
        #         return jsonify({"result": result})
    
    


# def get_all_workspaces():
    
#     return([1,2,3])

# def get_all_nodes():
    
#     return([1,2,4,3])



# db_api_dict={'workspaces':[('read',get_all_workspaces),'update'],
#              'nodes':['read','create','update','delete']}



def initialize_api_from_db_api_dict(app,db_api_dict):
    for k,v in db_api_dict.items():
        
        operations=[]
        if type(v)!=list:
            operations.append(v)
        else:
            operations=v
        #print(operations)
        for i,operation in enumerate(operations):
            if type(operation)==tuple:
                #print("A",operation)
                
                function=operation[1]
                operation=operation[0]
                
                #print("A",operation,function)
            else:
                function=lambda *x:print(*x)
                
                #print("B",operation,function)
        
            #print(operation,function)
            custom_endpoint=CustomEndpoint(app,k,operation,function)
            custom_endpoint.initialize_custom_endpoint()
            
#initialize_api_from_db_api_dict(app)

# custom_endpoint1=CustomEndpoint(app,"workspaces","read",get_all_workspaces)
# custom_endpoint1.initialize_custom_endpoint()
# custom_endpoint2=CustomEndpoint(app,"nodes","read",get_all_nodes)
# custom_endpoint2.initialize_custom_endpoint()


  
# import uvicorn

# def run_api():
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# if __name__=="__main__":
#     run_api()







def initialize_custom_endpoints(app,db_api_dict,column_names):
    """
    Example: 
        db_api_dict={'users':'read','items':['read','create']}
        column_names=["username","age"]
    
    """
    #for k,v in db_api_dict.items():
        


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
