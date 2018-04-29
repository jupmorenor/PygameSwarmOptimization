'''
Created on 11/05/2015
Updated on 29/04/2018

	-	enjambreParticulas.py
	
	Dependencias: 1. pygame
				  2. numpy (indirectamente)

@author: Juan Pablo Moreno Rico - 20111020059
'''
from __future__ import division
import os
from random import randint, seed, random as rnd
from math import sin, cos, atan2, radians, degrees
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame import surfarray 

DIRECTORIO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENTANA = (800,800)

def cargarImagen(path_):
	try:
		image_ = pygame.image.load(path_)#.convert_alpha()
	except pygame.error:
		print("No se encuentra la imagen " + path_)
		pygame.quit()
		raise(SystemExit)
	return image_

class Escritor():
	
	def __init__(self):
		self.fuente = pygame.font.Font(None, 30)
		
	def update(self, ventana, texto):
		self.texto = pygame.font.Font.render(self.fuente, texto, 1, pygame.color.Color("white"))
		ventana.blit(self.texto, self.texto.get_rect())
		
	
class EspacioSoluciones(object):
	"""
	Imagen plana que representa una funcion en 	el espacio 
	y la matriz que contiene los valores que corresponden
	"""
	def __init__(self, img):
		self.image = cargarImagen(img)
		self._espacio = surfarray.array2d(self.image) 
		
	def update(self, ventana):
		ventana.blit(self.image, (0,0))
		
	def __getitem__(self, pos):
		return self._espacio[pos[0]][pos[1]]
	
class Particula(pygame.sprite.Sprite):
	"""
	Particula que hace parte del enjambre
	"""
	def __init__(self, x_init, y_init, _id):
		pygame.sprite.Sprite.__init__(self)
		self.id = _id
		self.x = x_init
		self.y = y_init
		self.C1 = 2
		self.C2 = 2
		self.mejorLocal = [0,0,0]
		self.angulo = randint(0,359)
		self.imagenO = cargarImagen(os.path.join(DIRECTORIO, "img\part1.png"))
		self.image = self.imagenO
		self.rect = self.imagenO.get_rect()
		self.rect.center = self.x, self.y
		self.retraso = 0
	
	def rotar(self):
		self.image = pygame.transform.rotate(self.imagenO, self.angulo)
		self.rect = self.image.get_rect()
		self.rect.center = self.x, self.y
		
	def mover(self):
		self.x += cos(radians(self.angulo))*2
		self.y -= sin(radians(self.angulo))*2
		if (self.x >= VENTANA[0]):
			self.x = 0
		if (self.x < 0):
			self.x = VENTANA[0]-1
		if (self.y >= VENTANA[1]):
			self.y = 0
		if (self.y < 0):
			self.y = VENTANA[1]-1
		
	def update(self, ventana, espacio, mejorGlobal):
		"""
		self.C1 y self.C2 son coeficientes constantes
		rnd() es la aleatoriedad en el cambio de direccion
		"""
		self.rotar()
		self.mover()
		self.retraso += 0.1
		if self.retraso >= 1:
			self.angulo = (self.C1*rnd()*self.angDosPuntos(self.x, self.y, self.mejorLocal[1], self.mejorLocal[2]) 
			+ self.C2*rnd()*self.angDosPuntos(self.x, self.y, mejorGlobal[1], mejorGlobal[2]))
			self.retraso = 0
		if self.mejorLocal[0] < self.forma(espacio):
			self.mejorLocal[0] = max(self.forma(espacio), self.mejorLocal[0])
			self.mejorLocal[1] = self.x
			self.mejorLocal[2] = self.y
		if self.mejorLocal == mejorGlobal:
			self.imagenO = cargarImagen(os.path.join(DIRECTORIO, "img\part2.png"))
		ventana.blit(self.image, self.rect)
		
	def forma(self, espacio):
		return espacio[(int(self.x), int(self.y))]
	
	def angDosPuntos(self, x_1, y_1, x_2, y_2):
		y = y_2 - y_1
		x = x_2 - x_1
		ang = -degrees(atan2(y,x))
		if y<0:
			ang+=360
		return ang
		

class Enjambre(object):
	"""
	Enjambre conformado por n particulas
	"""
	def __init__(self, _n):
		self.n = _n
		self.mejorGlobal = [0,0,0]
		self.enjambre = []
		self.inicializar()
	
	def inicializar(self):
		for i in range(self.n):
			self.enjambre.append(Particula(randint(0,VENTANA[0]), randint(0,VENTANA[1]), i))
	
	def update(self, ventana, espacio):
		for particula in self.enjambre:
			particula.update(ventana, espacio, self.mejorGlobal)
			if self.mejorGlobal[0] < particula.mejorLocal[0]:
				self.mejorGlobal[0] = max(particula.mejorLocal[0], self.mejorGlobal[0])
				self.mejorGlobal[1] = particula.mejorLocal[1]
				self.mejorGlobal[2] = particula.mejorLocal[2]		

class Principal(object):
	
	def __init__(self):
		pygame.init()
		self.ventana = pygame.display.set_mode(VENTANA)
		seed()
		self.espacioSoluciones = EspacioSoluciones(os.path.join(DIRECTORIO, "img\\funcion.png"))
		self.enjambre = Enjambre(100)
		self.escritor = Escritor()
	
	def main(self):
		"""
		Control de la aplicacion
		"""
		pygame.display.set_caption("PSO - Pygame Swarm Optimization")
		reloj = pygame.time.Clock()
		
		while True:
			reloj.tick(30)
			for evento in pygame.event.get():
				if (evento.type == QUIT) or (evento.type==KEYDOWN and evento.key == K_ESCAPE):
					return 0
	
			self.espacioSoluciones.update(self.ventana)
			self.enjambre.update(self.ventana, self.espacioSoluciones)
			self.escritor.update(self.ventana, "MejorGlobal: " + str(self.enjambre.mejorGlobal))
			pygame.display.update()
		
		return 0

if __name__ == '__main__':
	app = Principal()
	app.main()
	pygame.quit()
