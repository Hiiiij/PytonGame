#Importieren der benoetigten Pakete

#import random Paket fuer zufalls zahlen 
import random
#import pygame Paket fuer unsere "game Engien"
import pygame
#import pymunk Paket fuer unsere "collision Engien"
import pymunk
#Praktische Methode zum Konvertieren lokaler Koordinaten der Pygame-Oberfläche in Pymunk-Koordinaten
import pymunk.pygame_util
#Die Vec2d-Klasse wird fast überall in Pymunk für 2D-Koordinaten und -Vektoren verwendet, um beispielsweise den Schwerkraftvektor in einem Raum zu definieren.
from pymunk import Vec2d
#Music (Sounds)
from pygame import mixer

Score = 0
PLAYZ = 52

PosFL = 200, 650
PosFR = 400, 650

inital = input("Wie stark soll der ball sein>")
inital = int(inital)


def main():
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    #def music()
    #import Hintergrund music
    
    pygame.mixer.music.load("music.mp3")
    #music Schleifen mit -1
    pygame.mixer.music.play(-1)
    #fenster Groesse setzen
    screen = pygame.display.set_mode((700, 800))
    height = pygame.display.Info().current_h
    width = pygame.display.Info().current_w
    LOGO = pygame.image.load('SuperGhostTransparent.png')
    pygame.display.set_icon(LOGO) 
    #pygame.time.Clock() als clock fuer kuertzere schreibweisen
    clock = pygame.time.Clock()
    running = True

    # Physics stuff
    space = pymunk.Space()
    space.gravity = (0.0, 1000.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    
    # Erstellen einer Galaxie Object Liste
    star_field_slow = []
    star_field_medium = []
    star_field_fast = []

    # Erstellen einer Ball Object Liste
    balls = []
    
    
    def call_begin(arbiter, space, data):
        balls = arbiter.shapes[1]
        bumper = arbiter.shapes[2]
        
        if arbiter.shapes[1].id == 2:
            print("punkt")
        else:
            print("nothing")
    # Erstellen einer Ball Lcollision fuer scoor
    #def ball_collision():
    #    print("hi")
    #   return True
     
    # Erstellen einer Ball function
    def create_ball(count=1):
        
            mass = 10
            radius = 12
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            x = random.randint(115, 350)
            body.position = 600, 500
            shape = pymunk.Circle(body, radius, (0, 0))
            shape.elasticity = 0.95
            space.add(body, shape)
            balls.append(shape)
            print(len(balls))
            shape.id = 1
            

            
    used_balls = 0

    # boost felder
    static_booster = [
        pymunk.Segment(space.static_body, (650, 600), (550, 600), 4.0),
    ]
    
    for line in static_booster:
        line.elasticity = inital
        line.group = 3
    space.add(*static_booster)

    
    # walls
    static_lines = [

        # Loundcher
        pymunk.Segment(space.static_body, (650, 200), (650, 600), 2.0),

        pymunk.Segment(space.static_body, (550, 50), (650, 200), 2.0),
        # reflector

        # spielbox
        pymunk.Segment(space.static_body, (50, 50), (50, 600), 2.0),
        pymunk.Segment(space.static_body, (550, 200), (550, 600), 2.0),

        # bottom
        pymunk.Segment(space.static_body, (50, 600), (200, height), 2.0),
        pymunk.Segment(space.static_body, (550, 600), (400, height), 2.0),

        # oben
        pymunk.Segment(space.static_body, (50, 50), (300, 0), 2.0),  # L
        pymunk.Segment(space.static_body, (300, 0), (550, 50), 2.0),  # R
        
        
        pymunk.Segment(space.static_body, (400, 650), (500, 600), 2.0),  # R
        pymunk.Segment(space.static_body, (200, 650), (100, 600), 2.0),  # L
        
        pymunk.Segment(space.static_body, (500, 600), (500, 500), 2.0),  # R
        pymunk.Segment(space.static_body, (100, 600), (100, 500), 2.0),  # L
        ]
        
    for line in static_lines:
        line.elasticity = 0.7
        line.group = 1
    space.add(*static_lines)

    fp = [(0, 0), (-80, 0), (0, 20)]
    mass = 100
    moment = pymunk.moment_for_poly(mass, fp)

    # right flipper
    r_flipper_body = pymunk.Body(mass, moment)
    r_flipper_body.position = PosFR
    r_flipper_shape = pymunk.Poly(r_flipper_body, fp)
    space.add(r_flipper_body, r_flipper_shape)

    r_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    r_flipper_joint_body.position = r_flipper_body.position
    j = pymunk.PinJoint(
        r_flipper_body, r_flipper_joint_body, (20, -20), (20, -20))
    # todo: tweak values of spring better
    s = pymunk.DampedRotarySpring(
        r_flipper_body, r_flipper_joint_body, -1, 20000000, 900000
    )
    space.add(j, s)

    # left flipper
    l_flipper_body = pymunk.Body(mass, moment)
    l_flipper_body.position = PosFL
    l_flipper_shape = pymunk.Poly(l_flipper_body, [(-x, y) for x, y in fp])
    space.add(l_flipper_body, l_flipper_shape)

    l_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    l_flipper_joint_body.position = l_flipper_body.position
    j = pymunk.PinJoint(l_flipper_body, l_flipper_joint_body,
                        (-20, -20), (-20, -20))
    s = pymunk.DampedRotarySpring(
        l_flipper_body, l_flipper_joint_body, 1, 20000000, 900000
    )
    space.add(j, s)

    r_flipper_shape.group = l_flipper_shape.group = 2
    r_flipper_shape.elasticity = l_flipper_shape.elasticity = 0.4

    # "bumpers"
    # (240, 100), (360, 100),
    bumpers = [(240, 100), (360, 100), (300, 300)]

    for p in bumpers:
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = p
        shape = pymunk.Circle(body, 20)
        shape.elasticity = 2
        space.add(body, shape)
        collisions_type = 2
        shape.id = 2
        
        def coll_begin(arbiter, space, data):
                print("hit")
                return True

        handler = space.add_default_collision_handler()
        handler.begin = coll_begin

        # Sternhimmel

    for slow_stars in range(50):  # birth those plasma balls, baby
        star_loc_x = random.randrange(0, width)
        star_loc_y = random.randrange(0, height)
        star_field_slow.append([star_loc_x, star_loc_y])  # i love your balls

    for medium_stars in range(35):
        star_loc_x = random.randrange(0, width)
        star_loc_y = random.randrange(0, height)
        star_field_medium.append([star_loc_x, star_loc_y])

    for fast_stars in range(15):
        star_loc_x = random.randrange(0, width)
        star_loc_y = random.randrange(0, height)
        star_field_fast.append([star_loc_x, star_loc_y])

    # define some commonly used colours
    WHITE = (255, 255, 255)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    WELCOME = pygame.mixer.Sound("WELCOME.wav")
    WELCOME.play()
    
    # Die gameLoop
    while running:
        
        hit = pygame.mixer.Sound("lr.wav")
                
        # die abfrage von Events (Tasten Strokes)
        for event in pygame.event.get():
            # goofy Ahh QuitFunction
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
                pygame.quit()
                quit()
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "Temporery_PyPinnBall.png")
                
                print("")

            # flipper Controles
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                hit.play()
                r_flipper_body.apply_impulse_at_local_point(
                    Vec2d.unit() * -20000, (-300, -20)
                )
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                hit.play()
                l_flipper_body.apply_impulse_at_local_point(
                    Vec2d.unit() * 20000, (-300, 20)
                )
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if used_balls < PLAYZ:
                    #used balls counter + 1 
                    used_balls += 1
                    #abrufen der ball function
                    create_ball()
                    #laden einer wav datei
                    start = pygame.mixer.Sound("start.wav")
                    #abspielen einer wav datei
                    start.play()
                else:
                    no = pygame.mixer.Sound("ni.wav")
                    #abspielen einer wav datei
                    no.play()
            
            
            
            
           

       # def coll_begin(arbiter, space, data):
         #   print("+100")
        #    return True

        #handler = space.add_default_collision_handler()
        #handler.begin = ball_collision

       # handler.beguin = coll_begin

        galaxy = pygame.image.load("background.png")
        screen.blit(galaxy, (0, 0))

        # s

        for star in star_field_slow:
            star[1] += 1
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, MAGENTA, star, 1)

        for star in star_field_medium:
            star[1] += 4
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, CYAN, star, 2)

        for star in star_field_fast:
            star[1] += 8
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, WHITE, star, 3)

         # Draw stuff
        space.debug_draw(draw_options)

        r_flipper_body.position = PosFR
        l_flipper_body.position = PosFL
        r_flipper_body.velocity = l_flipper_body.velocity = 0, 0

        # Remove any balls outside
        to_remove = []
        for ball in balls:
            if ball.body.position.get_distance((300, 300)) > 800:
                to_remove.append(ball)
                gone = pygame.mixer.Sound("gone.wav")
                gone.play()
                
                

        for ball in to_remove:
            space.remove(ball.body, ball)
            balls.remove(ball)

        # Update physics
        dt = 1.0 / 60.0 / 5.0
        for x in range(5):
            space.step(dt)

        # Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("Super Ghost Pinball running at fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    main()

