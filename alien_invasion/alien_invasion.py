import sys
import random
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from ship_shield import Ship_shield
from bullet import Bullet,Bullet_alien
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
    
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.ship_shield = Ship_shield(self)
        self.bullets = pygame.sprite.Group()
        self.bullets_alien = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the menu (difficulty)
        self.easy_button = Button(self,"Easy")

        self.medium_button = Button(self,"Medium")
        self.medium_button.new_button(self.easy_button)
        self.hard_button = Button(self,"Hard")
        self.hard_button.new_button(self.medium_button)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._fire_alien_bullet()

            if self.stats.game_active:
                self.ship.update()
                if self.settings.shield:
                    self.ship_shield.update(self.ship)
                self._update_bullets()
                self._update_alien_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_high_score(self.stats.high_score)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self,event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            update_high_score(self.stats.high_score)
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self,event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = (self.easy_button.rect.collidepoint(mouse_pos)
            or self.medium_button.rect.collidepoint(mouse_pos) or self.hard_button.rect.collidepoint(mouse_pos))
        #instruct_clicked = self.instruct_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings according to difficulty
            if self.easy_button.rect.collidepoint(mouse_pos):
                self.settings.initialize_dynamic_settings_easy()
            elif self.medium_button.rect.collidepoint(mouse_pos):
                self.settings.initialize_dynamic_settings_medium()
            elif self.hard_button.rect.collidepoint(mouse_pos):
                self.settings.initialize_dynamic_settings_hard()

            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship._center_ship()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of the bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        collisions = pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self.bullets_alien.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

            # Provide a shield every 2 level
            if self.stats.level%2 == 1:
                self.settings.shield = True

    def _fire_alien_bullet(self):
        """Create a new alien bullet and add it to the bullets_alien group"""
        if len(self.bullets_alien) < self.settings.alien_bullet_allowed:
            #alien = random.choice(self.aliens)
            for alien in self.aliens:
                if random.randint(1,10)==5:
                    new_bullet = Bullet_alien(self,alien)
                    self.bullets_alien.add(new_bullet)
                    break

    def _update_alien_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet position
        self.bullets_alien.update()

        # Get rid of the bullets that have disappeared
        for bullet_alien in self.bullets_alien.copy():
            if bullet_alien.rect.bottom >= self.settings.screen_width:
                self.bullets_alien.remove(bullet_alien)

        self._check_bullet_ship_collisions()

    def _check_bullet_ship_collisions(self):
        """Respond to bullet-ship collision"""
        if pygame.sprite.spritecollideany(self.ship,self.bullets_alien):
            self._ship_hit()

    def _update_aliens(self):
        """Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet. """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        # Look for aliens that hit the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the losing conditions"""
        if self.stats.ships_left > 0:
            if self.settings.shield:
                # Deactivate the shield and empty alien's bullets
                self.bullets_alien.empty()
                self.settings.shield = False
            else:
                # Decrement ships_left, and update scoreboard
                self.stats.ships_left -= 1
                self.sb.prep_ships()
                
                # Get rid of any aliens and remaining bullets
                self.aliens.empty()
                self.bullets.empty()
                self.bullets_alien.empty()

                # Create a new fleet and center the ship
                self._create_fleet()
                self.ship._center_ship()

                # Pause
                sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to 1 alien width
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2*alien_width
        number_alien_x = available_space_x // (2*alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3*alien_height) - ship_height
        number_rows = available_space_y // (2*alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        # Create an alien and place it in the row
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        if self.settings.shield:
            self.ship_shield.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        for bullet_alien in self.bullets_alien.sprites():
            bullet_alien.draw_bullet()

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

def update_high_score(new_high_score):
    """Update the high score via an external text file"""
    f = open("high_score.txt","r")
    old_high_score = int(float(f.read()))
    f.close()
    if new_high_score > old_high_score:
        f = open("high_score.txt","w")
        f.write(str(new_high_score))
        f.close()

        
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
