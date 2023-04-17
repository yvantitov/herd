import math
import random
import thorpy
import pygame

# display
SCREEN_H = 900
SCREEN_W = 900
FPS = 60
INF_OVERLAY_COLOR = (255, 0, 0, 100)

# starting populations
START_POP = 5000
START_INF = 1
START_IMM = START_POP * 0

# disease & transmission
RECOVERY_TIME = 10 * FPS
INF_RANGE = 15
INF_CHANCE = 0.03
MOV_SPD = 1


def clamp(n, min_val, max_val):
    return max(min(n, max_val), min_val)


class Qeeg:
    def __init__(self):
        self.pos_x = random.uniform(0, SCREEN_W)
        self.pos_y = random.uniform(0, SCREEN_H)
        self.infected = False
        self.infection_timeout = RECOVERY_TIME
        self.immune = False

    def infect(self):
        self.infected = True

    def update(self, screen, vulnerable, infected, immune, inf_overlay):
        pos_x_int = clamp(int(self.pos_x), 0, SCREEN_W - 1)
        pos_y_int = clamp(int(self.pos_y), 0, SCREEN_H - 1)

        if self.infected:
            self.infection_timeout -= 1
            if self.infection_timeout == 0:
                self.infected = False
                self.immune = True

                infected.remove(self)
                immune.append(self)
            else:
                pygame.draw.circle(inf_overlay, INF_OVERLAY_COLOR, (self.pos_x, self.pos_y), INF_RANGE)

        # check if we are on in the infection overlay
        elif inf_overlay.get_at((pos_x_int, pos_y_int)) == INF_OVERLAY_COLOR and not self.immune:
            roll = random.uniform(0, 1)
            if roll < INF_CHANCE:
                self.infect()
                vulnerable.remove(self)
                infected.append(self)

        # move the Qeeg
        vel_x = random.uniform(MOV_SPD * -1, MOV_SPD)
        rem_vel = MOV_SPD - abs(vel_x)
        vel_y = random.uniform(rem_vel * -1, rem_vel)
        self.pos_x = clamp(self.pos_x + vel_x, 0, SCREEN_W)
        self.pos_y = clamp(self.pos_y + vel_y, 0, SCREEN_H)

        # determine color
        color = (255, 255, 255)
        if self.infected:
            color = (255, 0, 0)
        if self.immune:
            color = (0, 255, 0)

        # draw the qeeg
        pygame.draw.circle(screen, color, (self.pos_x, self.pos_y), 1)


def main():
    pygame.init()

    logo = pygame.image.load("Caduceus.ico")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Herd")

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    inf_overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)

    clock = pygame.time.Clock()

    pop = list()
    vulnerable = list()
    infected = list()
    immune = list()
    for i in range(0, START_POP):
        q = Qeeg()
        if i < START_INF:
            q.infect()
            infected.append(q)
        elif i < START_IMM + START_INF:
            q.immune = True
            immune.append(q)
        else:
            vulnerable.append(q)
        pop.append(q)

    # declaration of some ThorPy elements ...
    stats = thorpy.make_text('test')
    box = thorpy.Box(elements=[stats])
    # we regroup all elements on a menu, even if we do not launch the menu
    menu = thorpy.Menu(box)
    # important : set the screen as surface for all elements
    for element in menu.get_population():
        element.surface = screen
    # use the elements normally...
    box.set_topleft((0, 0))
    box.blit()
    box.update()

    running = True
    sim_running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        if sim_running:
            inf_overlay.fill((0, 0, 0, 0))
            for q in infected:
                q.update(screen, vulnerable, infected, immune, inf_overlay)
            for q in vulnerable:
                q.update(screen, vulnerable, infected, immune, inf_overlay)
            for q in immune:
                q.update(screen, vulnerable, infected, immune, inf_overlay)

        screen.blit(inf_overlay, (0, 0))

        box.blit()
        box.update()

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
