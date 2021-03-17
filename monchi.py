import time
import arcade
import sys
from random import *

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 720
STRAWBERRY_SPRITE_SIZE = 0.02
STRAWBERRY_SPRITE_QUANTITY = 20
SPLATTER_SPRITE_SIZE = 0.1
POISON_SPRITE_SIZE = 0.05
POISON_SPRITE_QUANTITY = 8
MONCHI_SPRITE_SIZE = 0.15
TOMBSTONE_SPRITE_SIZE = 0.3
SCREEN_EDGE_BUFFER = 10
MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """ Main application class. """
    done = False
    failed = False
    drawCounter = 0

    def setup(self):
        self.strawberryList = arcade.SpriteList()
        self.splatterList = arcade.SpriteList()
        self.poisonList = arcade.SpriteList()
        self.monchiList = arcade.SpriteList()
        self.tombstoneList = arcade.SpriteList()
        self.strawberrySpeedList = [[randint(10,15), randint(0, 1), randint(0, 1), random()] for i in range(STRAWBERRY_SPRITE_QUANTITY)]
        self.poisonSpeedList = [[randint(10,15), randint(0, 1), randint(0, 1), random()] for i in range(POISON_SPRITE_QUANTITY)]
        self.strawberryPopSound = arcade.Sound("mixkit-water-bubble-1317.wav")
        self.monchiSplatSound = arcade.Sound("Spit_Splat-Mike_Koenig-1170500447.wav")
        for i in range(STRAWBERRY_SPRITE_QUANTITY):
            strawberry = arcade.Sprite("strawberry.png", STRAWBERRY_SPRITE_SIZE)
            strawberry.center_x = randint(1, SCREEN_WIDTH)
            strawberry.center_y = randint(1, SCREEN_HEIGHT)
            self.strawberryList.append(strawberry)
        
        for i in range(POISON_SPRITE_QUANTITY):
            poison = arcade.Sprite("poison.png", POISON_SPRITE_SIZE)
            poison.center_x = randint(1, SCREEN_WIDTH)
            poison.center_y = randint(1, SCREEN_HEIGHT)
            self.poisonList.append(poison)


        self.monchiSprite = arcade.Sprite("monchi.png", MONCHI_SPRITE_SIZE)
        self.monchiSprite.center_x = 920
        self.monchiSprite.center_y = 30
        self.monchiList.append(self.monchiSprite) 
        self.physicsEngine = arcade.PhysicsEngineSimple(self.monchiSprite, arcade.SpriteList())

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.AMAZON)

    def congratulate(self):
        self.done = True

    def moveSprites(self):
        for i in range(len(self.strawberryList)):
            speed = self.strawberrySpeedList[i]
            sprt = self.strawberryList[i]
            if (sprt.center_x + sprt.width / 2 >= SCREEN_WIDTH - SCREEN_EDGE_BUFFER) and speed[1] == 0:
                speed[1] = 1
            elif (sprt.center_x - sprt.width / 2 <= SCREEN_EDGE_BUFFER) and speed[1] == 1:
                speed[1] = 0
                
            if (sprt.center_y + sprt.height / 2 >= SCREEN_HEIGHT - SCREEN_EDGE_BUFFER) and speed[2] == 0:
                speed[2] = 1
            elif (sprt.center_y - sprt.height / 2 <= SCREEN_EDGE_BUFFER) and speed[2] == 1:
                speed[2] = 0
    
            movementX = speed[0] * speed[3]
            movementY = speed[0] * (1 - speed[3])
            if speed[1] == 1:
                movementX *= -1
            if speed[2] == 1:
                movementY *= -1
            self.strawberryList[i].change_x = movementX
            self.strawberryList[i].change_y = movementY
        
        for i in range(len(self.poisonList)):
            speed = self.poisonSpeedList[i]
            sprt = self.poisonList[i]
            if (sprt.center_x + sprt.width / 2 >= SCREEN_WIDTH - SCREEN_EDGE_BUFFER) and speed[1] == 0:
                speed[1] = 1
            elif (sprt.center_x - sprt.width / 2 <= SCREEN_EDGE_BUFFER) and speed[1] == 1:
                speed[1] = 0
                
            if (sprt.center_y + sprt.height / 2 >= SCREEN_HEIGHT - SCREEN_EDGE_BUFFER) and speed[2] == 0:
                speed[2] = 1
            elif (sprt.center_y - sprt.height / 2 <= SCREEN_EDGE_BUFFER) and speed[2] == 1:
                speed[2] = 0
    
            movementX = speed[0] * speed[3]
            movementY = speed[0] * (1 - speed[3])
            if speed[1] == 1:
                movementX *= -1
            if speed[2] == 1:
                movementY *= -1
            self.poisonList[i].change_x = movementX
            self.poisonList[i].change_y = movementY
            

    def on_draw(self):
        self.drawCounter = (self.drawCounter + 1) % 15
        if not self.failed and not self.done and self.drawCounter == 0:
            self.moveSprites()
            self.strawberryList.update()
            self.poisonList.update()

        arcade.start_render()        
        self.splatterList.draw()
        self.strawberryList.draw()
        self.poisonList.draw()
        self.monchiList.draw()
        self.tombstoneList.draw()
        start_x = SCREEN_WIDTH / 2
        start_y = SCREEN_HEIGHT - SCREEN_HEIGHT / 16
        arcade.draw_text("MONCHI!", start_x, start_y, arcade.color.BLACK, 30, width=500, align="center", font_name="BCTEXTEX", anchor_x="center", anchor_y="center")
        if self.failed:
            start_x = SCREEN_WIDTH / 2
            start_y = SCREEN_HEIGHT / 2
            arcade.draw_text("YOU LOST!", start_x, start_y, arcade.color.RED, 50, width=500, align="center", font_name="BCTEXTEX", anchor_x="center", anchor_y="center")
        elif self.done:
            start_x = SCREEN_WIDTH / 2
            start_y = SCREEN_HEIGHT / 2
            arcade.draw_text("CONGRATULATIONS!", start_x, start_y, arcade.color.PINK, 50, width=500, align="center", font_name="BCTEXTEX", anchor_x="center", anchor_y="center")


    def update(self, delta_time):
        if self.failed or self.done:
            return
        poisonContactList = arcade.check_for_collision_with_list(self.monchiSprite, self.poisonList)
        # Loop through each colliding sprite, remove it, and add to the score.
        for poison in poisonContactList:
            tombstone = arcade.Sprite("tombstone.png", TOMBSTONE_SPRITE_SIZE)
            tombstone.center_x = poison.center_x
            tombstone.center_y = poison.center_y
            self.monchiSprite.kill()
            self.tombstoneList.append(tombstone)
            self.monchiSplatSound.play()
            self.failed = True
      
        self.physicsEngine.update()
        monchedStrawberryList = arcade.check_for_collision_with_list(self.monchiSprite, self.strawberryList)
        # Loop through each colliding sprite, remove it, and add to the score.
        for strawberry in monchedStrawberryList:
            splatter = arcade.Sprite("splatter.png", SPLATTER_SPRITE_SIZE)
            splatter.center_x = strawberry.center_x
            splatter.center_y = strawberry.center_y
            strawberry.kill()
            self.splatterList.append(splatter)
            self.strawberryPopSound.play()
            
        if len(self.strawberryList) == 0:
            self.congratulate()

    def inSprite(self, x, y, sprite):
        left = sprite.center_x - (sprite.width / 2)
        right = sprite.center_x + (sprite.width / 2)
        bottom = sprite.center_y - (sprite.height / 2)
        top = sprite.center_y + (sprite.height / 2)
        return x > left and x < right and y > bottom and y < top
    
    def on_mouse_press(self, x, y, button, modifiers):
        if (self.done or self.failed) and button == arcade.MOUSE_BUTTON_LEFT:
            self.close()


    def on_key_press(self, key, modifiers):        
        if (self.monchiSprite.center_y <= 50 and key == arcade.key.DOWN) or (self.monchiSprite.center_y >= SCREEN_HEIGHT - 50 and key == arcade.key.UP):
            self.monchiSprite.change_y = 0
        else:
            if key == arcade.key.UP:
                self.monchiSprite.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.monchiSprite.change_y = -MOVEMENT_SPEED
        
        if (self.monchiSprite.center_x <= 50 and key == arcade.key.LEFT) or (self.monchiSprite.center_x >= SCREEN_WIDTH - 50 and key == arcade.key.RIGHT):
            self.monchiSprite.change_x = 0
        else:
            if key == arcade.key.LEFT:
                self.monchiSprite.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.monchiSprite.change_x = MOVEMENT_SPEED
        



    
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.monchiSprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.monchiSprite.change_x = 0


def main():
    while(True):
        game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
        game.setup()
        arcade.run()


if __name__ == "__main__":
    main()
