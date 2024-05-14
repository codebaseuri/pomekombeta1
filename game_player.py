

import db_and_security_functions as sf
class player_position():
    def __init__(self,name,x_cord,y_cord):
        self.x_cord=x_cord
        self.y_cord=y_cord
        self.name=name
        self.current_picure=0
        self.current_direction="down"
    def __repr__(self):
        return f"name='{self.name}',x,y='{self.x_cord,self.y_cord}')"
        
class create_player_data():
    def __init__(self, name,password,email):
        self.name = name
        self.password=password
        self.email=email
        self.x_cord=500
        self.y_cord=500
        self.current_picure=0
        self.current_direction="down"
        #self.friends={}
        #self.items={}
        #self.pokemos={}
    def __repr__(self):
        return f"name='{self.name}', password='{self.password}', email='{self.email},x,y='{self.x_cord,self.y_cord}')"
class msg_signup():
    def __init__(self,msg):
        try:
            self.msg=msg.split(b"~")
            self.method=self.msg[0]
            self.username=self.msg[1]
            self.password=self.msg[2]
            self.email=self.msg[3]
            
        except:
            print("erorr in creating signup msg")

class msg_login(): 
    def __init__(self,msg):
        try:
            self.msg=msg.split(b"~")
            self.method=self.msg[0]
            self.username=self.msg[1]
            self.password=self.msg[2]
        except:
            print("erorr in creating login msg")

class messging_msg():
    def __init__(self,msg):
        try:
            self.msg=msg.split(b"~")
            self.method=self.msg[0] 
            self.src_name=self.msg[1]
            self.dest_name=self.msg[2]
            self.message=self.msg[3]# cotains the content of the message

        except:
            print("erorr in creating login msg")
if __name__=="__main__":
    p=create_player_data(1,2,3)
    print(p.__repr__())