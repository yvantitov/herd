import math
import random
import thorpy
import pygame


def clamp(n, min_val, max_val):
    return max(min(n, max_val), min_val)


class Qeeg:
    def __init__(self, herd):
        self.herd = herd

        self.pos_x = random.uniform(self.herd.menu_w, self.herd.screen_w)
        self.pos_y = random.uniform(0, self.herd.screen_h)
        self.infected = False
        self.infection_timeout = 0
        self.immunity_timeout = 0
        self.immune = False

    def infect(self):
        self.infected = True
        self.immune = False
        self.infection_timeout = self.herd.recovery_time

    def update(self):
        pos_x_int = clamp(int(self.pos_x), self.herd.menu_w, self.herd.screen_w - 1)
        pos_y_int = clamp(int(self.pos_y), 0, self.herd.screen_h - 1)

        if self.infected:
            if self.infection_timeout != 0:
                self.infection_timeout -= 1
                if self.infection_timeout == 0:
                    roll = random.uniform(0, 1)
                    if roll < self.herd.fatality_rate:
                        self.herd.pop.remove(self)
                        self.herd.infected.remove(self)
                        return
                    else:
                        self.infected = False
                        self.immune = True
                        self.immunity_timeout = self.herd.immunity_time
                        self.herd.infected.remove(self)
                        self.herd.immune.append(self)

        if self.immune:
            if self.immunity_timeout != 0:
                self.immunity_timeout -= 1
                if self.immunity_timeout == 0:
                    self.immune = False
                    self.herd.immune.remove(self)
                    self.herd.vulnerable.append(self)

        # check if we are on in the infection overlay
        if self.herd.inf_overlay.get_at((pos_x_int, pos_y_int)) == self.herd.inf_overlay_color and not self.infected:
            roll = random.uniform(0, 1)
            min_roll = self.herd.inf_chance
            if self.immune:
                min_roll = self.herd.inf_chance_imm
            if roll < min_roll:
                if self.immune:
                    self.herd.immune.remove(self)
                else:
                    self.herd.vulnerable.remove(self)
                self.infect()
                self.herd.infected.append(self)

        if self.infected:
            pygame.draw.circle(
                self.herd.inf_overlay,
                self.herd.inf_overlay_color,
                (self.pos_x, self.pos_y),
                self.herd.inf_range)

        # move the Qeeg
        vel_x = random.uniform(self.herd.mov_spd * -1, self.herd.mov_spd)
        rem_vel = self.herd.mov_spd - abs(vel_x)
        vel_y = random.uniform(rem_vel * -1, rem_vel)
        self.pos_x = clamp(self.pos_x + vel_x, self.herd.menu_w, self.herd.screen_w)
        self.pos_y = clamp(self.pos_y + vel_y, 0, self.herd.screen_h)

        # determine color
        color = (255, 255, 255)
        if self.infected:
            color = (255, 0, 0)
        if self.immune:
            color = (0, 255, 0)

        # draw the qeeg
        pygame.draw.circle(self.herd.screen, color, (self.pos_x, self.pos_y), 1)


class Herd:
    def __init__(self):
        # display
        self.menu_w = 300
        self.screen_h = 900
        self.screen_w = 1100
        self.fps = 60
        self.inf_overlay_color = (255, 0, 0, 100)

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.inf_overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        pygame.display.set_caption("Herd")

        # disease & transmission
        self.recovery_time = 10 * self.fps
        self.immunity_time = 10 * self.fps
        self.inf_range = 15
        self.inf_chance = 0.03
        self.inf_chance_imm = 0
        self.mov_spd = 1
        self.fatality_rate = 0.5

        # UI
        self.stats_pop = thorpy.make_text("")
        self.stats_inf = thorpy.make_text("")
        self.stats_imm = thorpy.make_text("")
        self.stats_ded = thorpy.make_text("")
        self.slider_recovery_time = thorpy.SliderX(120, (0, 20), "Recovery time (s)", initial_value=10)
        self.slider_immunity_time = thorpy.SliderX(120, (0, 20), "Immunity time (s)", initial_value=10)
        self.slider_inf_range = thorpy.SliderX(120, (1, 30), "Infection range", initial_value=self.inf_range)
        self.slider_inf_chance = thorpy.SliderX(120, (0, 1), "Infection chance", initial_value=self.inf_chance)
        self.slider_inf_chance_imm = thorpy.SliderX(
            120,
            (0, 1),
            "^ (when immune)",
            initial_value=self.inf_chance_imm)
        self.slider_mov_spd = thorpy.SliderX(120, (0.5, 5), "Move speed", initial_value=self.mov_spd)
        self.slider_fatality_rate = thorpy.SliderX(120, (0, 1), "Fatality rate", initial_value=self.fatality_rate)
        self.pause = thorpy.make_button("Play", func=self.toggle_pause)
        self.start_pop_box = thorpy.Inserter("Starting population", value="5000")
        self.start_inf_box = thorpy.Inserter("Starting infected", value="1")
        self.start_imm_slider = thorpy.SliderX(120, (0, 100), "Starting immune %", initial_value=20, type_=int)
        self.restart = thorpy.make_button("Restart", func=self.regen_game)

        self.box = thorpy.Box(size=(self.menu_w, self.screen_h), elements=[
            self.stats_pop,
            self.stats_inf,
            self.stats_imm,
            self.stats_ded,
            self.slider_recovery_time,
            self.slider_immunity_time,
            self.slider_inf_range,
            self.slider_inf_chance,
            self.slider_inf_chance_imm,
            self.slider_mov_spd,
            self.slider_fatality_rate,
            self.pause,
            self.start_pop_box,
            self.start_inf_box,
            self.start_imm_slider,
            self.restart])
        thorpy.store(self.box, x=10, y=0, align='left')

        self.menu = thorpy.Menu(self.box)
        for element in self.menu.get_population():
            element.surface = self.screen
        self.box.set_topleft((0, 0))
        self.box.blit()
        self.box.update()

        # starting populations
        self.start_pop = 5000
        self.start_inf = 1
        self.start_imm = self.start_pop * 0

        self.pop = list()
        self.vulnerable = list()
        self.infected = list()
        self.immune = list()
        self.regen_game()

        # control
        self.running = True
        self.sim_running = False
        self.clock = pygame.time.Clock()

    def regen_game(self):
        try:
            self.start_pop = int(self.start_pop_box.get_value())
            self.start_inf = int(self.start_inf_box.get_value())
        except ValueError:
            self.start_inf = 1
            self.start_pop = 5000
            self.start_inf_box.set_value("1")
            self.start_pop_box.set_value("5000")
        self.start_imm = (self.start_imm_slider.get_value() / 100) * self.start_pop

        self.pop = list()
        self.vulnerable = list()
        self.infected = list()
        self.immune = list()
        for i in range(0, self.start_pop):
            q = Qeeg(self)
            if i < self.start_inf:
                q.infect()
                self.infected.append(q)
            elif i < self.start_imm + self.start_inf:
                q.immune = True
                q.immunity_timeout = self.immunity_time
                self.immune.append(q)
            else:
                self.vulnerable.append(q)
            self.pop.append(q)
        self.screen.fill((0, 0, 0))
        self.inf_overlay.fill((0, 0, 0, 0))
        for q in self.pop:
            q.update()
        self.screen.blit(self.inf_overlay, (0, 0))

    def update_stats(self):
        self.stats_pop.set_text("Population: %d" % len(self.pop))
        self.stats_inf.set_text("Infected: %d" % len(self.infected))
        self.stats_imm.set_text("Immune: %d" % len(self.immune))
        self.stats_ded.set_text("Deaths: %d" % (self.start_pop - len(self.pop)))

    def toggle_pause(self):
        self.sim_running = not self.sim_running
        if self.sim_running:
            self.pause.set_text("Pause")
        else:
            self.pause.set_text("Play")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.toggle_pause()
                self.menu.react(event)

            if self.sim_running:
                self.screen.fill((0, 0, 0))
                self.inf_overlay.fill((0, 0, 0, 0))
                for q in self.infected:
                    q.update()
                for q in self.vulnerable:
                    q.update()
                for q in self.immune:
                    q.update()
                self.screen.blit(self.inf_overlay, (0, 0))

            self.update_stats()

            self.recovery_time = self.slider_recovery_time.get_value() * self.fps
            self.immunity_time = self.slider_immunity_time.get_value() * self.fps
            self.inf_range = self.slider_inf_range.get_value()
            self.inf_chance = self.slider_inf_chance.get_value()
            self.inf_chance_imm = self.slider_inf_chance_imm.get_value()
            self.mov_spd = self.slider_mov_spd.get_value()
            self.fatality_rate = self.slider_fatality_rate.get_value()

            self.box.blit()
            self.box.update()

            pygame.display.flip()

            self.clock.tick(60)


if __name__ == "__main__":
    h = Herd()
    h.run()
