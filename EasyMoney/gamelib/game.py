#! /usr/bin/env python
#game
import sys, os


import pygame
from pygame.locals import *

from cutscenes import *
from data import *
from sprites import *
from level import *

def RelRect(actor, camera):
    return Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

class Camera(object):
    def __init__(self, player, width):
        self.player = player
        self.rect = pygame.display.get_surface().get_rect()
        self.world = Rect(0, 0, width, 480)
        self.rect.center = self.player.rect.center

    def update(self):
        if self.player.rect.centerx > self.rect.centerx+64:
            self.rect.centerx = self.player.rect.centerx-64
        if self.player.rect.centerx < self.rect.centerx-64:
            self.rect.centerx = self.player.rect.centerx+64
        if self.player.rect.centery > self.rect.centery+64:
            self.rect.centery = self.player.rect.centery-64
        if self.player.rect.centery < self.rect.centery-64:
            self.rect.centery = self.player.rect.centery+64
        self.rect.clamp_ip(self.world)
    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))


class Game(object):

    def __init__(self, screen, continuing=False):

        self.screen = screen
        self.sprites = pygame.sprite.OrderedUpdates()
        self.players = pygame.sprite.OrderedUpdates()
        self.platforms = pygame.sprite.OrderedUpdates()
        # self.grays = pygame.sprite.OrderedUpdates()
        self.bricks = pygame.sprite.OrderedUpdates()
        # self.movingplatforms = pygame.sprite.OrderedUpdates()
        # self.movingplatformtwos = pygame.sprite.OrderedUpdates()
        self.nomoveplatforms = pygame.sprite.OrderedUpdates()
        self.coins = pygame.sprite.OrderedUpdates()
        self.playerdying = pygame.sprite.OrderedUpdates()
        self.springs = pygame.sprite.OrderedUpdates()
        # self.platformqs = pygame.sprite.OrderedUpdates()

        Player.right_images = [load_image("perso1.png"), load_image("perso2.png"), load_image("perso3.png"), load_image("perso4.png"), load_image("perso1.png"), load_image("perso5.png")]
        Platform.images = {"platform-top.png": load_image("platform-top.png"), "platform-middle.png": load_image("platform-top.png")}
        # Grass.images = {"grass-1.png": load_image("grass-1.png"), "grass-middle.png": load_image("grass-middle.png")}
        # Gray.images = {"gray1.png": load_image("gray1.png"), "gray2.png": load_image("gray2.png")}
        Brick.images = {"brick2.png": load_image("brick2.png")}
        # MovingPlatform.image = load_image("moving-platform.png")
        # MovingPlatformtwo.image = load_image("moving-platformlong.png")
        Coin.images = [load_image("coin%s.png" % i) for i in range(1, 5)]
        CoinDie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        PlayerDie.right_images = [load_image("persodie.png"), load_image("exp2-1.png"), load_image("exp2-2.png"), load_image("exp2-3.png")]
        Spring.images = [load_image("spring1.png"), load_image("spring2.png")]
        Spring2.images = [load_image("spring3.png"), load_image("spring4.png")]
        # AirPlatform.image = load_image("platform-air.png")
        # PlatformQ.images = [load_image("platform-q%s.png" % i) for i in range (1, 4)]

        Player.groups = self.sprites, self.players
        Platform.groups = self.sprites, self.platforms, self.nomoveplatforms
        Brick.groups = self.sprites, self.bricks, self.nomoveplatforms
        # Gray.groups = self.sprites, self.grays, self.nomoveplatforms
        # MovingPlatform.groups = self.sprites, self.platforms, self.movingplatforms
        # MovingPlatformtwo.groups = self.sprites, self.platforms, self.movingplatformtwos
        Coin.groups = self.sprites, self.coins
        CoinDie.groups = self.sprites
        PlayerDie.groups = self.sprites, self.playerdying
        Spring.groups = self.sprites, self.springs
        Spring2.groups = self.sprites, self.springs
        # AirPlatform.groups = self.sprites, self.platforms, self.nomoveplatforms
        # PlatformQ.groups = self.sprites, self.platformqs, self.nomoveplatforms, self.platforms
        # Platform_Brick.groups = self.sprites, self.platforms, self.nomoveplatforms
        # Grasstexture.groups = self.sprites, self.platforms, self.nomoveplatforms
        # Grass1.groups = self.sprites, self.platforms, self.nomoveplatforms
        # Grass2.groups = self.sprites, self.platforms, self.nomoveplatforms
        # GrassSprite.groups = self.sprites
        # Wall.groups = self.sprites
        # Lava.groups = self.sprites
        # Bridge.groups = self.sprites, self.platforms, self.nomoveplatforms
        # Chain.groups = self.sprites,

        self.highscore = 0
        self.score = 0
        self.lives = 1
        self.lvl   = 1
        if continuing:
            self.lvl = 1
        self.player = Player((0, 0))
        self.clock = pygame.time.Clock()
        self.bg = load_image("background.png")
        self.level = Level(self.lvl)
        self.camera = Camera(self.player, self.level.get_size()[0])
        self.font = pygame.font.SysFont("Carlito", 16)
        self.time = 180
        self.running = 1
        if not continuing:
            cutscene(self.screen,
                     ['Note: Utilisez les fleches',
                      'directionnelles pour vous deplacez',
                      'Appuyez sur Z pour sauter'])

        self.intro_level()
        self.main_loop()

    def end(self):
        self.running = 0

    def intro_level(self):
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        pygame.display.flip()
        pygame.time.wait(2500)

    # def redo_level(self):
    #     self.booming = False
    #     # self.boom_timer = 0
    #     self.time = 180
    #     if self.running:
    #         self.clear_sprites()
    #         self.level = Level(self.lvl)
    #         self.player = Player((0, 0))
    #         self.camera = Camera(self.player, self.level.get_size()[0])
    #         self.score -= self.score
    #         self.highscore = self.highscore
    #         play_music("maintheme.ogg")
    #         # if self.lvl == 5:
    #         #     play_music("castle.ogg")

    # def show_death(self):
    #     ren = self.font.render("YOU DIED", 1, (255, 255, 255))
    #     self.screen.blit(ren, (320-ren.get_width()/2, 235))
    #     pygame.display.flip()
    #     pygame.time.wait(2500)

    # def show_end(self):
    #     play_music("goal.ogg")
    #     pygame.time.wait(7500)
    #     pygame.display.flip()

    def score_screen(self):
        cutscene(self.screen, ["Your score: %05d" % self.score])
        self.end()


    # def clear_sprites(self):
    #     for s in self.sprites:
    #         pygame.sprite.Sprite.kill(s)

    def main_loop(self):

        while self.running:
            # BaddieShot.player = self.player
            if not self.running:
                return

            self.clock.tick(60)
            self.camera.update()
            for s in self.sprites:
                s.update()

            for p in self.platforms:
                p.update()
            self.player.collide(self.springs)
            self.player.collide(self.platforms)

            for b in self.bricks:
                b.update()
            self.player.collide(self.bricks)


            # for l in self.grays:
            #     l.update()
            # self.player.collide(self.grays)

            for c in self.coins:
                if self.player.rect.colliderect(c.rect):
                    c.kill()
                    CoinDie(c.rect.center)
                    self.score += 50

            # for p in self.movingplatformtwos:
            #     p.collide(self.players)
            #     for p2 in self.platforms:
            #         if p != p2:
            #             p.collide_with_platforms(p2)
            #
            # for p in self.movingplatforms:
            #     p.collide(self.players)
            #     for p2 in self.platforms:
            #         if p != p2:
            #             p.collide_with_platforms(p2)

            # if self.player.rect.right > self.camera.world.w:
            #     if not self.bombs and self.lvl < 30:
            #         self.next_level()
            #     else:
            #         self.player.rect.right = self.camera.world.w
            #
            # if self.player.rect.right > self.camera.world.w:
            #     if not self.bombs and self.lvl < 30:
            #         self.next_level()
            #     else:
            #         self.player.rect.right = self.camera.world.w

            # if self.player.rect.right > self.camera.world.w:
            #     self.next_level()


            if self.player.alive():
                self.time -= 0.013
            if self.time <= 0:
                self.player.hit()

            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.end()
                    if e.key == K_z:
                        self.player.jump()
                    if e.key == K_UP:
                        self.player.jump()
            if not self.running:
                return
            self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640, 0))
            self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640 + 640, 0))
            self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640 - 640, 0))
            self.camera.draw_sprites(self.screen, self.sprites)
            self.draw_stats()

            if not self.player.alive() and not self.playerdying:
                 if self.lives <= 1:
                     self.score_screen()
                 else:
                    self.show_death()
                    self.lives -= 1
                    self.redo_level()
            pygame.display.flip()
            if not self.running:
                return

    def draw_stats(self):

        lives = self.lives
        if lives < 0:
            lives = 0
        ren = self.font.render("Score: %05d" % self.score, 1, (255, 255, 255))
        self.screen.blit(ren, (624-ren.get_width(), 16))
        ren1 = self.font.render("Time: %d" % self.time, 1, (255, 255, 255))
        self.screen.blit(ren1, (485, 60))
