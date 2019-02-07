import os, pygame
from pygame.locals import *

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

def filepath(filename):
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):

    return open(os.path.join(data_dir, filename), mode)

def load_image(filename):
	filename = filepath(filename)
	try:
		image = pygame.image.load(filename)
		image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
	except pygame.error:
		raise SystemExit() and "Unable to load: " + filename
	return image.convert_alpha()
