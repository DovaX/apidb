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


def add_function_parameter(add_function_parameter):
    def decorator(f):
        
        
        
        f.__name__ = add_function_parameter
        return f
    return decorator



class CustomEndpoint:
    def __init__(self,app,name,operation,function,body_template,api_url="/api/",id_variable="id",show_method_tags=True,show_endpoint_tags=True):
        self.app=app
        self.name=name #should be in plural
        self.operation=operation
        self.function=function
        self.body_template = body_template
        self.api_url=api_url
        self.id_variable=id_variable
        self.show_method_tags=show_method_tags
        self.show_endpoint_tags=show_endpoint_tags
        self.operation_method_tag_dict={"read_all":"get","read":"get","create":"post","delete":"delete","delete_all":"delete","update":"put"}
      
         
    def initialize_custom_endpoint(self):
        tags=[]
        body_template = self.body_template
        if self.show_endpoint_tags:
            tags+=[self.name.capitalize()+" Methods"]
        if self.show_method_tags:
            tags+=[self.operation_method_tag_dict[self.operation].capitalize()+" Methods"]
    
        if 'read_all'==self.operation:
            @self.app.get(self.api_url+self.name,tags=tags)
            @rename_function('read_all_'+self.name)
            def read_all_items():
                result=self.function()
                return {"result":result}
        
        if 'read'==self.operation:
            item=self.name[:-1]
            @self.app.get(self.api_url+item+"/{"+self.id_variable+"}",tags=tags)
            @rename_function('read_'+item)
            def read_item(uid): #TODO: generalize uid for any variable name
                result=self.function(uid) 
                return {"result":result}
    
    
        if 'create'==self.operation:
            item=self.name[:-1]
            @self.app.post(self.api_url+item,tags=tags)
            @rename_function('create_'+item)
            def add_item(body_template:body_template):
                params = [getattr(body_template, field) for field in body_template.dict().keys()]
                result = self.function(params)
                return {"result":result}
                # return {}
            
        if 'update'==self.operation:
            item=self.name[:-1]
            @self.app.put(self.api_url+item+"/{"+self.id_variable+"}",tags=tags)
            @rename_function('update_'+item)
            def update_item(uid, body_template:body_template):
                params = [uid] + [getattr(body_template, field) for field in body_template.dict().keys()]
                result=self.function(params)
                return {"result":result}
        
            
        if 'delete'==self.operation:
            item=self.name[:-1]
            @self.app.delete(self.api_url+item+"/{"+self.id_variable+"}",tags=tags)
            @rename_function('delete_'+item)
            def delete_item(uid):
                result=self.function(uid)
                return {"result":result}
            
            
            
        if 'delete_all'==self.operation:
            @self.app.delete(self.api_url+self.name,tags=tags)
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
        #
        #         cur.execute("UPDATE "+self.name+" SET "+column_names[0]+" = '" + str(column1) + "' where id = " + id)
        #         mysql.connection.commit()
        #         result = {column_names[0]:column1}
        #
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



def initialize_api_from_db_api_dict(app,db_api_dict,api_url="/api/",id_variable="id"):
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

                body_template = operation[2]
                function=operation[1]
                operation=operation[0]

                #print("A",operation,function)
            else:
                function=lambda *x:print(*x)
                
                #print("B",operation,function)
        
            #print(operation,function)
            custom_endpoint=CustomEndpoint(app,k,operation,function,body_template,api_url=api_url,id_variable=id_variable)
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
            @app.put("/api/"+k+"/{id}")
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
            @app.delete("/api/"+k+"/{id}")
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
