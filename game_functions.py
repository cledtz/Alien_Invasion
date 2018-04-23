import sys
from time import sleep

import pygame

#import ship
from bullet import Bullet
from missile import Missile
from alien import Alien


#### BULETS ####

def fire_bullet(ai_settings, screen, ship, bullets):
    """Create a new bullet and add it to the bullets group."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
        
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    

#### MISSILES ####

def fire_missile(ai_settings, screen, ship, missiles):
    """Create a new missile and add it to the missiles group."""
    if len(missiles) < ai_settings.missiles_allowed:
        new_missile = Missile(ai_settings, screen, ship)
        missiles.add(new_missile)
        

def update_missiles(missiles):
    """Update position of bullets and get rid of old bullets."""
    # Update missile position.
    missiles.update()
    
    # Get rid of missiles that have disappeared.
    for missile in missiles.copy():
        if missile.rect.bottom <= 0:
            missiles.remove(missile)
        



#### BULLETS & MISSILES ####

def empty_shoots(missiles, bullets):
    bullets.empty()
    missiles.empty()


def check_collisions_b(ai_settings, screen, stats, sb, ship, aliens, bullets, missiles):
    """Respond to bullet/missile - alien collisions"""
    # Remove any bullets and aliens that have collided.
    b_collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    for aliens in b_collisions.values():
        stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
    check_high_score(stats, sb)
    
    if len(aliens) == 0:
        empty_shoots(missiles, bullets)
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
    
def check_collisions_m(ai_settings, screen, stats, sb, ship, aliens, bullets, missiles):
    """Respond to bullet/missile - alien collisions"""
    # Remove any bullets and aliens that have collided.
    m_collisions = pygame.sprite.groupcollide(missiles, aliens, False, True)
    for aliens in m_collisions.values():
        stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
    check_high_score(stats, sb)
    
    if len(aliens) == 0:
        empty_shoots(missiles, bullets)
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
    


#### ALIENS ####

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - alien_width
    number_aliens_x = int(available_space_x/(1.5 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - ship_height - (5 * alien_height))
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien.x = alien.rect.width/2 * (2 + (-1) ** row_number) + 1.5 * alien.rect.width * alien_number
    alien.y = 50 + alien.rect.height/2 + 1.5 * alien.rect.height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    alien.direction *= (-1)**row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change direction to every alien."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
        alien.direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
    
def update_aliens(ai_settings, aliens):
    """
    Check if the fleet is at an edge,
        and then update the position of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    

def empty_aliens(aliens):
    aliens.empty()

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, missiles, bullets):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        sb.prep_ships()
        empty_shoots(missiles, bullets)
        empty_aliens(aliens)
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alien_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, missiles, bullets):
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, missiles, bullets)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, missiles, bullets):
    """Check if any aliens reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, missiles, bullets)

#### KEY PRESSES / RELESES ####

def respond_to_keydown_events(event, ai_settings, stats, screen, ship, bullets, missiles):
    """Respond to key-presses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_m:
        fire_missile(ai_settings, screen, ship, missiles)
    elif event.key == pygame.K_q:
        sys.exit()
    

def respond_to_keyup_events(event, ship):
    """Respond to key-releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
                    

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, missiles, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if not stats.game_active and button_clicked:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Empty the list of aliens, bullets, and missiles.
        aliens.empty()
        bullets.empty()
        missiles.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, missiles):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                respond_to_keydown_events(event, ai_settings, stats, screen, ship,
                                          bullets, missiles)
                    
            elif event.type == pygame.KEYUP:
                respond_to_keyup_events(event, ship)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, missiles, mouse_x, mouse_y)


#### SCREEN ####

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, missiles, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # Redraw the ship, missiles and aliens.
    ship.blitme()
    missiles.draw(screen)
    aliens.draw(screen)
    
    # Draw the score information.
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
        
    #Make the most recently drawn screen visible.
    pygame.display.flip()
    
    
def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()