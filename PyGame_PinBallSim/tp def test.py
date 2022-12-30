from turtle import*
from random import*
# Importiere von turtle und random

color("purple")
shape("circle")
tracer(0)
# Visuelle beschreibund des Balles

width = input("Breite")
heigth = input("Hoehe")
energy = input("Energy")
# Eingabe Der Grundwerte

width = int(width)
heigth = int(heigth)
energy = int(energy)
# Integer Convertirung

velosetyY = energy
velosetyX = energy
# Das momentum aud der x und y Achse Wird auf den selben wert Energie gesetzt was bedeutet
# das sich der ball wie eine liniare function mit einer steigung von 45 grad bewegt

drag = 0.2
grav = -0.5
x=0
y=0
# Die w
def tp(x,y):
    penup()
    goto(x,y)
    pendown()
    # Text text text
    
def Box(width,heigth):
    penup()
    backward(width/2)
    left(90)
    backward(heigth/2)
    pendown()
    # Text text text
    forward(heigth)
    right(90)
    forward(width)
    right(90)
    forward(heigth)
    right(90)
    forward(width)
    # Erstellen einer szalierbaren Box mit collison
    
Box(width,heigth)


while True:
    
    x = x+velosetyX
    y = y+velosetyY
    tp(x,y)
    # bewegen des balles 
    
    if x > width/2 or x < -width/2:
        velosetyX = -velosetyX
        color("green")
        # Collision auf der x-achse
        energy = energy - 0.1
        
    if y > heigth/2 or y < -heigth/2:
        velosetyY = -velosetyY
        color("red")
        print("L")
        # Collision auf der y-achse
        
    update()
    # update der werte!
   