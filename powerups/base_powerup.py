import pygame, unit, helper, bmpfont, effects
from pygame.sprite import Sprite

FRAME_MOVE_SPEED = 3/20
SIZE = 20

class powerup(Sprite):
    """
    The basic representation of a power up from which all other powerup types
    extend. Has a graphical representation and is stationary at specific
    locations on the map, and other units can consume it.
    
    Note: self._base_image MUST be set in subclasses! This is the tilesheet
    from which the unit renders its actual image.
    """
    
    active_units = pygame.sprite.LayeredUpdates()
    
    def __init__(self,
                 tile_x = None,
                 tile_y = None,
                 angle = 0,
                 activate = False,
                 **keywords):
        Sprite.__init__(self)

        # Take the keywords off
        self.tile_x = tile_x
        self.tile_y = tile_y
        self._angle = angle

        #set required pygame things.
        self.image = None
        self.rect = pygame.Rect(0, 0, SIZE, SIZE)
        self._update_image()
        
        if activate:
            self.activate()

    @property
    def tile_pos(self):
        """
        Returns the unit's tile position.
        """
        return (self.tile_x, self.tile_y)

    def _update_image(self):
        """
        Re-renders the powerup's image.
        """
        # Pick out the right sprite depending on the team
        subrect = pygame.Rect(self.team * SIZE,
                              0,
                              self.rect.w,
                              self.rect.h)
        try:
            subsurf = self._base_image.subsurface(subrect)
        except ValueError:
            # No sprite for this team
            raise ValueError(
                "Class {} does not have a sprite for team {}!".format(
                    self.__class__.__name__, self.team))
        except AttributeError:
            # No image is loaded
            return
        
        # Rotate the sprite
        self.image = pygame.transform.rotate(subsurf, self._angle)

    def activate(self):
        """
        Adds this unit to the active roster.
        """
        if not self._active:
            self._active = True
            BaseUnit.active_units.add(self)
    
    def deactivate(self):
        """
        Removes this unit from the active roster.
        """
        if self._active:
            self._active = False
            BaseUnit.active_units.remove(self)