from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, asynchronous, gen
from tornado.escape import xhtml_escape
import motor

db = motor.MotorClient().pruebaTornado # esto obtiene la base de datoss

class MainHandler(RequestHandler):
    def get(self):
      self.write("hola")

class CreateUser(RequestHandler):
  def get(self):
    self.write('<html><body><form action="/user" method="post">'
		   'Nombre: <input type="text" name="Nombre"><BR>'
                   'Usuario: <input type="text" name="Usuario"><BR>'
                   'Constrasena: <input type="text" name="Contrasena"><BR>'
                   '<input type="submit" value="create">'
                   '</form></body></html>')
  @asynchronous  
  def post(self):
    #conexion con la base de datos
    nombre = self.get_argument('Nombre')
    usuario = self.get_argument('Usuario')
    contrasena = self.get_argument('Contrasena')
    self.settings['db'].usuarios.insert({'nombre':nombre,'usuario':usuario,'contrasena':contrasena},callback=self.respuesta)
  
  def respuesta(self,result,error):
    if error:
      raise tornado.web.HTTPError(500,error)
    else:
      self.redirect('/')
   
class Login(RequestHandler):
  def get(self):
    self.write('<html><body><form action="/login" method="post">'
                   'Usuario: <input type="text" name="Usuario"><BR>'
                   'Constrasena: <input type="text" name="Contrasena"><BR>'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')
  @gen.coroutine
  def post(self):
    #aqui va la autentificacion
    usuario = self.get_argument('Usuario')
    contrasena = self.get_argument('Contrasena')
    resultado = yield self.settings['db'].usuarios.find_one({'usuario': usuario, 'contrasena': contrasena})
    if resultado:
     self.write("usuario encontrado")
    else:
     self.redirect('/login')
    

application = Application([
    (r"/", MainHandler),
    (r"/user",CreateUser),
    (r"/login",Login)
],db=db)

def main():
  
  application.listen(8888)
  IOLoop.instance().start()
  

if __name__ == "__main__":
    main()