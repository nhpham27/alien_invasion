import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(((self.settings.screen_width, self.settings.screen_height)))
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        pygame.display.set_caption("Alien Invasion")
        
        # create statistics object to save game stats
        self.stats = GameStats(self)

        # create instance of the ship
        self.ship = Ship(self)
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        """ Full screen mode
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        """

    def _ship_hit(self):
        """Respond to the ship being hit by the alien"""
        if self.stats.ships_left > 0:
            # decrement ship_left
            self.stats.ships_left -= 1

            # remove aliens and bullets
            self.bullets.empty()
            self.aliens.empty()

            # create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # pause the game
            sleep(0.5)    
        else:
            self.stats.game_active = False

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_event()
            if self.stats.game_active:
                self.ship.update()
                self._update_shooting()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _update_shooting(self):
        if self.ship.shooting_rate > 1:
            self._fire_bullet()
            self.ship.shooting_rate = 0

    def _check_fleet_edges(self):
        """check if any alien has reached the edges"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the fleet and change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 

    def _update_aliens(self):
        """ check if the aliens have reached the edges and
            update the position of all the aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()
        
        # check if the ship collide the aliens
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """create the fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2*alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine nu,ber of rows fit the screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 8 * alien_height - ship_height
        number_rows = available_space_y // (2*alien_height)
        # create first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_aliens(alien_number, row_number)
    
    def _create_aliens(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_bullets(self):
        """Update the bullets"""
        self.bullets.update()
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):   
        # remove disapeared bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        # check if any bullet has hit the aliens
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        # if there is no alien left
        # clear the bullets and create a new fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _check_event(self):
        # watch for keyboard and mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.ship.is_shooting = True

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.ship.is_shooting = False

    def _fire_bullet(self):
        """Create new bullet and add to the sprite group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        # Draw the ship on the game screen
        self.ship.blitme()

        # update the bullets' movements
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # draw the aliens
        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()