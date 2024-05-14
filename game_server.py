import pickle
import db_and_security_functions as db
import game_player 
starting_dir = r"D:\final_networking_project"
databasename="datastore.pickle"
db_path=databasename
import threading
import connection as con
lock=threading.Lock()
from connection import recv_by_size
from connection import send_by_size 
import threading
import socket
import collections

class server:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip,port))
        self.s.listen(6)
        print("server started")


    def parse_reply(self,msg):    
        return input("enter you reply ")  
        #this function will receive will protocol command was sent and parse a reply acordinglly

    def handle_client(self,serv_cleint):
        msg=recv_by_size(serv_cleint,"bytes")   
        print(msg)

        

        while True:
          
            msg=recv_by_size(serv_cleint,"bytes")   
            #print("recvied msg")
            print(msg)
           
            reply=self.parse_reply(msg)
            print(reply)
            #after implementing this function 
            if b"quit" in msg:
                print ("this clie niggernt has finished his business")  
                serv_cleint.close()
                break  
            else :
                continue
            


    def accept_cleints(self):
        threads=[]
        tid=0   
        while True:
            try:
                self.serv_cleint,self.addr=self.s.accept()  
                thread=threading.Thread(target=self.handle_client,args=[self.serv_cleint]) 
                thread.start()
                threads.append(thread)
                print("new client")
                tid += 1       
            except socket.error as err:
                print('socket error', err)
                break
                exit_all = True
                for t in threads:
                    t.join()

class user_server(server):
    def __init__(self,ip,port):
        
        super().__init__(ip,port)
        self.game_started=False
        self.online_Users={}
        self.pending_messages = collections.deque()
        print("1")
        print(db_path)
        #GAME_players is dictionary that holds all the players who currently are active in the game
        self.datastore=db.load_data(db_path)
        print(self.datastore)
        print("2")
        #this loads the data from the pickle file
        #now game server will be waiting for players to connect

    def check_isexist(self,username):
        return username in self.datastore
    
    def sign_up(self,username,password,email):
        
        if not self.check_isexist(username):
            player=game_player.create_player_data(username,password,email)
            #checks if a player with that username already exists
            # if npot create a new player
            
            with lock:
                self.datastore[username]=player 
                print(f"player{username} signed up")
                db.save_data(self.datastore,db_path)
            return True
        else:
            print("username already exists")
            return False

    def login(self,username,password):
        #print("the password is ",password)
        #print("the password stored is ",self.datastore[username].password)

        if username in self.datastore and self.datastore[username].password==password:
            
            if  username not in self.online_Users:
                print("3\n")
                with lock:
                    self.online_Users[username]=self.serv_cleint
                    print(f"player {username} logged in succsefully")
                    var=self.return_online_players_cords(username)
                    
                return True,pickle.dumps((var,0))# returns the player data object 
            else:
                print("username or password is incorrect or player already logged in ")
                return False,b""
        return False,b""

    def return_online_players_cords(self,username):
        dict1={}
        for key in self.online_Users.keys():
            if key!=username:
                dict1[key]=self.datastore[key]
        print("returning.... "+dict1.__repr__())
        player_cords=game_player.player_position(username,self.datastore[username].x_cord,self.datastore[username].y_cord)
        print(player_cords.__repr__())
        return player_cords



    def deliver_message(self,msg):
        print(msg)
        msg_string=msg
        msg=game_player.messging_msg(msg)
        
        if msg.dest_name in self.online_Users and msg.src_name in self.online_Users:
            try:
               print(msg.message)
               con.send_by_size(self.online_Users[msg.dest_name],pickle.dumps(msg))
               print(f"message sent to {msg.dest_name} sucssesfully")
               return "message sent successfully"
            

            except Exception as e:
                print(e)
                print("failed to deliver message")
                return "failed to deliver message"

        else:
            return "user not online unable to send message"
        
    def recv_player_data(self,msg):
        
            msg=msg.split(b"~")
            with lock:
                player_data=pickle.loads(msg[1])

                self.datastore[player_data.name]=player_data
            #print("rararara")
            print(player_data.__repr__())
            #updates player information to the dictionary 
            self.broadcast_players(msg[1],player_data.name)
        # send to all the player the updatated data about this player 

    def broadcast_players(self,player_data,username):
        #need to remove own player from the list
        #print("entered brodcast")    
        with lock:
            #print(self.online_Users)
            for player in self.online_Users:
                if player!=username:
                    con.send_by_size(self.online_Users[player], player_data)
                    print(f"message sent to {player} sucssesfully")
                

    
    def get_key_from_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

    def innitalize_battle(self,msg):
        msg=msg.split(b"~")
        player1=msg[1]
        player2=msg[2]
        print(player1,player2)
        p1="battle_query~".encode()+player1
        var=pickle.dumps(p1)
        #print(var)
        with lock:
            send_by_size(self.online_Users[player2],var)
        
        
    
    def return_battle_query(self,player_name,server_cleint):
        return   
    def check_yesin_query(self,server_cleint): 
        current_tuple=None
        with lock:
            for _ in range(len(self.pending_messages)):
                current_tuple = self.pending_messages.popleft()  # Pop the leftmost tuple
                if b'yes' in current_tuple:
                    #print(self.online_Users[current_tuple[1]])
                    #print(current_tuple[1])
                    #print(self.serv_cleint)

                    if self.online_Users[current_tuple[1]]==server_cleint:
                        print("entered poped tuple")
                        popped_tuple = current_tuple  # Store the tuple in the variable
                        return True
                    else:
                        self.pending_messages.append(current_tuple)
                        #print("helpppppp")
                        #print(self.pending_messages)
                else:
                    self.pending_messages.append(current_tuple)
                    #print(self.pending_messages)
        return False

    def handle_client(self,serv_cleint):


        while True:
            #print(serv_cleint)
            if self.check_yesin_query(serv_cleint):
                send_by_size(serv_cleint,pickle.dumps("query_responce~yes".encode()))
                print("sent query responce to destination")
            try:
                msg=recv_by_size(serv_cleint,"bytes",timeout=1)
            except Exception as e:
                break
            #print(msg)
            if b"quit" in msg:

                print("it seem scleint is not responding will now close connection ")
                with lock:
                    if serv_cleint in self.online_Users.values():
                        
                        key=self.get_key_from_value(self.online_Users,serv_cleint)
                        print(key,serv_cleint)
                        del self.online_Users[key]
                    serv_cleint.close()
                    break
                
            elif b"win"in msg:
                msg=msg.split(b"~") 
                print(f"player{msg[1]} won the battle!")
                
                
            elif b"login"in msg:
                login_msg=game_player.msg_login(msg)
                login_data=self.login(login_msg.username,login_msg.password)
                if login_data[0]:
                    send_by_size (serv_cleint,login_data[1])
                else:
                    send_by_size (serv_cleint,"login failed")
                
            

            elif b"signup"in msg:

                signup_msg=game_player.msg_signup(msg)
                print(signup_msg.method , signup_msg.username , signup_msg.password , signup_msg.email)

                if self.sign_up(signup_msg.username,signup_msg.password,signup_msg.email):
                    #print(f"signed up of {signup_msg.username} was successful")
                    send_by_size (self.serv_cleint,"signup successful")


            # need to fix up messaging between players!!!!!!!!!!!!.   
            elif b"message" in msg:
                print(self.deliver_message(msg))
            # this is for player to comunicate with each other

            elif b"move" in msg:
                #update all player on updates player position
                pass

            elif b"battle_request" in msg:
                responce=self.innitalize_battle(msg)
                print(responce)

            elif b"query_responce" in msg:
                with lock:
                    if b"yes" in msg: 
                        msg=msg.split(b"~")
                        print(msg)
                        self.pending_messages.append((msg[2],msg[3],msg[1]))
                    elif b"yes"not in msg: 
                        self.pending_messages.append((msg[2],msg[3],msg[1]))
                    

            elif b"player_data" in msg:
                try:
                    self.recv_player_data(msg)
                except Exception as e:
                    print(e)
                    print("failed to update player data")

                #update all player on updates player position
                pass
            elif b"battle" in msg:

                #battle keep track of the battle between to players
                pass
              
            else :
                continue
            #splited_msg=msg.split(b"~")

        
if __name__ == '__main__':
    game_serveR=user_server("0.0.0.0",1234)
    game_serveR.accept_cleints()
#game_serveR=game_server()
#game_serveR.foo2()
#server=server('0.0.0.0', 1234)    
#server.accept_cleints()