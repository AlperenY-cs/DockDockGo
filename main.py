#DockDockGo v1.0

#If you want this api, you have must have docker installed on your system.
#Bu api'yi kullanmak istiyorsanız sisteminizde Docker kurulu olmalıdır.

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import docker as dk

client = dk.from_env()
#Docker deamon ile etkileşime geçmek için oluşturuldu.
#Connection with Docker deamon.
  
app = Flask(__name__)
# creating the flask app
api = Api(app)
# creating an API object
  

class Hello(Resource):
  
    def get(self):  
        return jsonify({'message': 'Netcom Rocks!'})
  
class Run(Resource):   
#Container ayağa kaldırmak için kullanılan path: /run
#The path used to boot the container: /run
    
    def get(self):  
        
        try:            
            container = client.containers.run("kalilinux/kali-rolling", tty=True, detach=True, ports={5000: None})
            #kali-rolling image'ını kullanır, arka planda çalışır halde kalması için tty ve detach parametreleri verilir. Rastgele port ataması için None kullanılır.
            
            container.reload() #Yeni data için yeniden yükleme yapar.               
            
            ip_addr = container.attrs['NetworkSettings']['IPAddress']
            #Container attributes kullanarak IPAddress değerine ulaşır.
            
            port = container.attrs["NetworkSettings"]['Ports']
            #Container attributes kullanarak Ports değerine ulaşır. 
        
            return jsonify ({'id':container.short_id, 'status': container.status, 'name': container.name, 'ip': ip_addr, 'port':port})           
            #short_id, status, name, ip ve port değerlerini döndürür.
        
            
        except:     
            return jsonify ({'Error': "Container couldn't start."})        
            # Container sorunsuz başlamazsa hata mesajı dönderecek.
         

class IpAddr(Resource):
#Ip ve port bilgisine ulaşmak için kullanılan path: /ip?id=[container short_id]
    
    def get(self):
        try:
            id_parameter_from_url = request.args.get('id')
            #url'den id parametresini alır.
            
            containerClient = client.containers.get(id_parameter_from_url)
            #Id değeri alınan container ve methodları containerClient değişkenine atanır. 
        
            ip_address = containerClient.attrs['NetworkSettings']['IPAddress']
            #ContainerClient attributes kullanarak IPAddress değerine ulaşır.
            
            port = containerClient.attrs["NetworkSettings"]['Ports']
            #ContainerClient attributes kullanarak Ports değerine ulaşır. 
        
            return jsonify ({'ip': ip_address, 'port': port})
        except:
            return jsonify ({'Error':"Ip address couldn't show."})        
         
  
#Eklenen pathler
api.add_resource(Hello,'/')
api.add_resource(Run,'/run')
api.add_resource(IpAddr,'/ip')
  

if __name__ == '__main__':
  
    app.run(debug = True)
