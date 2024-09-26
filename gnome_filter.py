import pygame
import cv2
from PIL import Image
import math
import sys

capture = cv2.VideoCapture(0) # opens camera using cv2
faceCascade = cv2.CascadeClassifier(sys.path[0]+'/face_cascade.xml')

width, height = 1024, 512

pygame.init() # initiates pygame window
clock = pygame.time.Clock()
running = True
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Gnome')

#gnome image
gnome_face = pygame.image.load(sys.path[0]+'/gnome.png')

while running:
    
    # allows program to quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    surface.fill('black')
    
    #captures frame
    frame = capture.read()[1]
        
    #converts frame to image
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
    # detects faces
    faces = faceCascade.detectMultiScale(
		cv2image,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
    )
        
    # changes cv2 to pygame surface
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    pillow_img = Image.fromarray(cv2image)
    img_data = pillow_img.tobytes()
    img_dimensions = pillow_img.size
    img = pygame.image.fromstring(img_data, img_dimensions, 'RGB')
    img = pygame.transform.flip(img, True, False) 
    img = pygame.transform.scale(img, (width, height))
    
    surface.blit(img, (0,0)) # adds image as background
    
    for (x, y, w, h) in faces: # interates through faces on the screen
        
        x, y, w, h = width-math.floor(w/img_dimensions[0]*width)-math.floor(x/img_dimensions[0]*width), math.floor(y/img_dimensions[1]*height), math.floor(w/img_dimensions[0]*width), math.floor(h/img_dimensions[1]*height) # gets dimensions of gnome based off camera dimensions
        
        changed_face = pygame.transform.scale(gnome_face, (w, h)) 
        surface.blit(changed_face, (x, y)) # updates imgae with overlay
    
    # renders screen
    pygame.display.flip()
    
    clock.tick(10)