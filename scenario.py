import pygame


class Scenario:
    def __init__(
            self,
            name,
            img,
            recovery_time,
            immunity_time,
            inf_range,
            inf_chance,
            inf_chance_imm,
            mov_spd,
            fatality_rate,
            start_pop,
            start_inf,
            start_imm
    ):
        self.name = name
        self.img = img
        self.recovery_time = recovery_time
        self.immunity_time = immunity_time
        self.inf_range = inf_range
        self.inf_chance = inf_chance
        self.inf_chance_imm = inf_chance_imm
        self.mov_spd = mov_spd
        self.fatality_rate = fatality_rate
        self.start_pop = start_pop
        self.start_inf = start_inf
        self.start_imm = start_imm

    def apply_preview(self, herd):
        herd.scenario_title.set_text(self.name)
        herd.scenario_img.set_image(pygame.image.load(self.img))

    def apply(self, herd):
        herd.recovery_time = self.recovery_time
        herd.slider_recovery_time.set_value(self.recovery_time)

        herd.immunity_time = self.immunity_time
        herd.slider_immunity_time.set_value(self.immunity_time)

        herd.inf_range = self.inf_range
        herd.slider_inf_range.set_value(self.inf_range)

        herd.inf_chance = self.inf_chance
        herd.slider_inf_chance.set_value(self.inf_chance)

        herd.inf_chance_imm = self.inf_chance_imm
        herd.slider_inf_chance_imm.set_value(self.inf_chance_imm)

        herd.mov_spd = self.mov_spd
        herd.slider_mov_spd.set_value(self.mov_spd)

        herd.fatality_rate = self.fatality_rate
        herd.slider_fatality_rate.set_value(self.fatality_rate)

        herd.start_pop = self.start_pop
        herd.start_pop_box.set_value(str(self.start_pop))

        herd.start_inf = self.start_inf
        herd.start_inf_box.set_value(str(self.start_inf))

        herd.start_imm = self.start_imm
        herd.start_imm_slider.set_value(self.start_imm)

        herd.regen_game()
        herd.update_stats()


curr_scenario = 0

scenarios = [Scenario(
    "Black Death",
    "scen_black_death.png",
    2.5,
    0,
    13,
    0.15,
    0,
    1,
    0.6,
    10000,
    1,
    0
), Scenario(
    "Common Cold",
    "scen_common_cold.png",
    1,
    2.15,
    30,
    0.03,
    0,
    1.9,
    0,
    5000,
    1,
    0
), Scenario(
    "Herd Immunity",
    "scen_herd_immunity.png",
    2.5,
    0,
    13,
    0.15,
    0,
    1.9,
    0,
    5000,
    1,
    95
)]
