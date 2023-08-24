import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion - 1337 Remake")

    # Create an instance to stare game statistics, and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Deploy", stats)
    play_again_button = Button(ai_settings, screen, "Try again..", stats)

    # Make a group to store bullets in.
    bullets = Group()

    # Make a group to store bullets in.
    alien_bullets = Group()

    # Make a group to store missiles in.
    missiles = Group()

    # Make a ship.
    ship = Ship(ai_settings, screen)

    # Make a group to store aliens in.
    aliens = Group()

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens, stats)

    # Start the main loop for game.
    while True:

        # Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, missiles, play_again_button)


        # Update ship, bullets, missiles, aliens.
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets)
            gf.alien_update_bullets(alien_bullets, ai_settings)
            gf.update_missiles(missiles)
            gf.check_collisions_b(ai_settings, stats, sb, aliens, bullets, missiles, alien_bullets)
            gf.check_collisions_m(ai_settings, stats, sb, aliens, bullets, missiles, alien_bullets)
            gf.check_collisions_s(ai_settings, screen, stats, sb, ship, aliens, bullets, missiles, alien_bullets)
            gf.update_aliens(ai_settings, aliens, screen, alien_bullets, stats)
            gf.remove_expired(aliens)
            gf.check_alien_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, missiles, bullets, alien_bullets)
            gf.check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, missiles, bullets, alien_bullets)
        else:
            gf.empty_aliens(aliens)
            gf.empty_shoots(missiles, bullets, alien_bullets)


        # Redraw the screen during each pass through the loop.
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, missiles, play_button, play_again_button)



if __name__ == "__main__":
    run_game()