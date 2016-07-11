from math import sin, cos
import sys
import time
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import BitMask32
from panda3d.core import NodePath
from panda3d.core import PandaNode
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from panda3d.bullet import BulletWorld, YUp
from panda3d.bullet import BulletHelper
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletSoftBodyNode
from panda3d.bullet import BulletSoftBodyConfig
from panda3d.bullet import BulletHingeConstraint
from panda3d.bullet import ZUp
from math import trunc
from panda3d.core import TransparencyAttrib
loadPrcFileData("", "win-size 1366 768")

def onscreenText(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale=.05)

class CharacterController(ShowBase):

    # add damage mechanic for player vs enamy and enamy vs player
    # will i make player in super mode not take dmg from enamy ?

    def __init__(self):
        ShowBase.__init__(self)

        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)
        base.disableMouse()

        self.setupLights()

        # Input
        self.accept('escape', self.doExit)
        self.accept('r', self.doReset)
        self.accept('f3', self.toggleDebug)
        self.accept('space', self.doJump)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')

        inputState.watchWithModifiers('camLeft', 'arrow_left')
        inputState.watchWithModifiers('camRight', 'arrow_right')
        inputState.watchWithModifiers('camUp', 'arrow_up')
        inputState.watchWithModifiers('camDown', 'arrow_down')

        self.volume = .5

        self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()

        self.setup()

        # Used in Level Design
        self.cx = onscreenText(.95, '')
        self.cy = onscreenText(.90, '')
        self.cz = onscreenText(.85, '')

        # Task
        taskMgr.add(self.update, 'updateWorld')

    def buildLevel(self):

        size = Vec3(3, 3, 1)
        position = Vec3(200, 0, 0)
        self.createFloatingRectangle(size, position, 'P1')

        size = Vec3(6, .5, 1)
        position = Vec3(180, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.1', (30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(160, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.2', (-30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(140, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.3', (30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(120, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.4', (-30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(100, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.5', (30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(80, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.6', (-30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(60, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.7', (30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(40, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.8', (-30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(20, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.9', (30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(0, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.10', (-30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(-20, 0, 0)
        self.createFloatingRectangle(size, position, 'P1.10', (30, 0, 0))

        size = Vec3(100, 100, 1)
        position = Vec3(-132, 0, 0)
        self.createFloatingRectangle(size, position, 'P2')

        size = Vec3(50, 50, 30)
        position = Vec3(-132, 0, 31)
        self.createFloatingRectangle(size, position, 'P2.1')

        size = Vec3(35, 35, 15)
        position = Vec3(-132, 0, 76)
        self.createFloatingRectangle(size, position, 'P2.2')

        size = Vec3(20, 20, 8)
        position = Vec3(-132, 0, 99)
        self.createFloatingRectangle(size, position, 'P2.3')

        size = Vec3(3, 3, 1)
        position = Vec3(-119, 60, 66)
        self.createFloatingRectangle(size, position, 'P2.4')

        size = Vec3(3, 3, 1)
        position = Vec3(-135, 60, 71)
        self.createFloatingRectangle(size, position, 'P2.5')

        size = Vec3(3, 3, 1)
        position = Vec3(-119, 60, 76)
        self.createFloatingRectangle(size, position, 'P2.6')

        size = Vec3(3, 3, 1)
        position = Vec3(-135, 60, 81)
        self.createFloatingRectangle(size, position, 'P2.7')

        size = Vec3(3, 3, 1)
        position = Vec3(-119, 60, 86)
        self.createFloatingRectangle(size, position, 'P2.8')

        size = Vec3(3, 3, 1)
        position = Vec3(-90, -8, 95)
        self.createFloatingRectangle(size, position, 'P2.9')

        size = Vec3(3, 3, 1)
        position = Vec3(-70, -8, 100)
        self.createFloatingRectangle(size, position, 'P2.10')

        size = Vec3(3, 3, 1)
        position = Vec3(-85, 10, 105)
        self.createFloatingRectangle(size, position, 'P2.11')

        size = Vec3(49, 3, 1)
        position = Vec3(-135, -53, 12.8)
        self.createFloatingRectangle(size, position, 'P2.12', (0,0,15))

        size = Vec3(3, 3, 1)
        position = Vec3(-185, -53, 25.45)
        self.createFloatingRectangle(size, position, 'P2.13')

        size = Vec3(3, 49, 1)
        position = Vec3(-185, -3, 38.1)
        self.createFloatingRectangle(size, position, 'P2.14', (0,15,0))

        size = Vec3(3, 6, 1)
        position = Vec3(-185, 50, 50.8)
        self.createFloatingRectangle(size, position, 'P2.15')

        size = Vec3(18, 3, 1)
        position = Vec3(-164.5, 53, 55.4)
        self.createFloatingRectangle(size, position, 'P2.16', (0,0,-15))

        size = Vec3(3, 3, 1)
        position = Vec3(-144.5, 53, 60)
        self.createFloatingRectangle(size, position, 'P2.17')

        size = Vec3(12, 12, 1)
        position = Vec3(-250, 3, 20)

        self.createFloatingRectangle(size, position, 'P2.18')

        size = Vec3(9, 3, 1)
        position = Vec3(-91, -53, 20)

        self.createFloatingRectangle(size, position, 'P2.19')


        size = Vec3(3, 3, 1)
        position = Vec3(-400, -6, 123)

        self.createFloatingRectangle(size, position, 'P3')


        size = Vec3(3, 3, 1)
        position = Vec3(-180, -6, 105)

        self.createFloatingRectangle(size, position, 'P3.1')

        size = Vec3(3, 3, 1)
        position = Vec3(-209, -6, 105)

        self.createFloatingRectangle(size, position, 'P3.2')

        size = Vec3(3, 3, 1)
        position = Vec3(-238, 6, 105)

        self.createFloatingRectangle(size, position, 'P3.3')

        size = Vec3(3, 3, 1)
        position = Vec3(-238, -18, 105)

        self.createFloatingRectangle(size, position, 'P3.4')

        size = Vec3(3, 3, 1)
        position = Vec3(-267, -30, 105)

        self.createFloatingRectangle(size, position, 'P3.5')

        size = Vec3(3, 3, 1)
        position = Vec3(-267, 18, 105)

        self.createFloatingRectangle(size, position, 'P3.6')

        size = Vec3(3, 3, 1)
        position = Vec3(-296, 30, 105)

        self.createFloatingRectangle(size, position, 'P3.7')

        size = Vec3(3, 3, 1)
        position = Vec3(-296, -42, 105)

        self.createFloatingRectangle(size, position, 'P3.8')

        size = Vec3(3, 3, 1)
        position = Vec3(-325, -54, 100)

        self.createFloatingRectangle(size, position, 'P3.9')

        size = Vec3(3, 3, 1)
        position = Vec3(-325, 42, 100)

        self.createFloatingRectangle(size, position, 'P3.10')

        size = Vec3(3, 3, 1)
        position = Vec3(-325, 18, 105)

        self.createFloatingRectangle(size, position, 'P3.11')

        size = Vec3(3, 3, 1)
        position = Vec3(-325, -30, 105)

        self.createFloatingRectangle(size, position, 'P3.12')

        size = Vec3(3, 3, 1)
        position = Vec3(-354, -18, 105)

        self.createFloatingRectangle(size, position, 'P3.13')

        size = Vec3(3, 3, 1)
        position = Vec3(-354, 6, 105)

        self.createFloatingRectangle(size, position, 'P3.14')

        size = Vec3(3, 3, 1)
        position = Vec3(-383, -6, 105)

        self.createFloatingRectangle(size, position, 'P3.15')

        size = Vec3(3, 3, 1)
        position = Vec3(-315, -9, 80)

        self.createFloatingRectangle(size, position, 'P3.16')

        size = Vec3(9, 9, 1)
        position = Vec3(-325, -90, 100)

        self.createFloatingRectangle(size, position, 'P3.17')

        size = Vec3(9, 9, 1)
        position = Vec3(-325, 78, 100)

        self.createFloatingRectangle(size, position, 'P3.18')

        size = Vec3(3, 3, 1)
        position = Vec3(-400, -6, 111)

        self.createFloatingRectangle(size, position, 'P3.19')

        size = Vec3(3, 3, 1)
        position = Vec3(-383, -6, 117)

        self.createFloatingRectangle(size, position, 'P3.20')

        size = Vec3(3, 3, 1)
        position = Vec3(-400, -6, 123)

        self.createFloatingRectangle(size, position, 'P3')

    def addItems(self):

        #Waypoints

        position = Vec3(-40, 0, 5)
        self.createConsumables(position, 0, 1)

        position = Vec3(-131, 2, 111)
        self.createConsumables(position, 0, 2)

        #Finish

        position = Vec3(-400, -5, 140)
        self.createConsumables(position, -1, 1)

        #Time

        position = Vec3(184.5, 3, 3)
        self.createConsumables(position, 2, 1)

        position = Vec3(175.4, -2.7, 3)
        self.createConsumables(position, 4, 1)

        position = Vec3(164.8, -2.5, 3)
        self.createConsumables(position, 2, 2)

        position = Vec3(155.5, 2.54, 3)
        self.createConsumables(position, 4, 2)

        position = Vec3(144.7, 2.9, 3)
        self.createConsumables(position, 2, 3)

        position = Vec3(135.7, -2.7, 3)
        self.createConsumables(position, 4, 3)

        position = Vec3(124.7, -2.7, 3)
        self.createConsumables(position, 2, 4)

        position = Vec3(104.8, 2.7, 3)
        self.createConsumables(position, 4, 4)

        position = Vec3(115.5, 2.5, 3)
        self.createConsumables(position, 2, 5)

        position = Vec3(95.5, -2.5, 3)
        self.createConsumables(position, 4, 5)

        position = Vec3(84.9, -3.0, 3)
        self.createConsumables(position, 2, 6)

        position = Vec3(75.7, 2.6, 3)
        self.createConsumables(position, 4, 6)

        position = Vec3(65.0, 2.5, 3)
        self.createConsumables(position, 2, 7)

        position = Vec3(55.1, -2.6, 3)
        self.createConsumables(position, 4, 7)

        position = Vec3(45.7, -2.9, 3)
        self.createConsumables(position, 4, 8)

        position = Vec3(33.3, 2.6, 3)
        self.createConsumables(position, 4, 9)

        position = Vec3(25.9, 2.6, 3)
        self.createConsumables(position, 2, 8)

        position = Vec3(15.2, -2.8, 3)
        self.createConsumables(position, 4, 10)

        position = Vec3(5.2, -2.8, 3)
        self.createConsumables(position, 2, 9)

        position = Vec3(-4.5, 2.5, 3)
        self.createConsumables(position, 4, 11)

        position = Vec3(-15.2, 2.5, 3)
        self.createConsumables(position, 2, 10)

        position = Vec3(-24.4, -2.6, 3)
        self.createConsumables(position, 4, 12)

        position = Vec3(-243.5, -4.74, 25)
        self.createConsumables(position, 4, 13)

        position = Vec3(-242.0, 11.63, 25)
        self.createConsumables(position, 4, 14)

        position = Vec3(-258.0, -5.8, 25)
        self.createConsumables(position, 4, 15)

        position = Vec3(-258.0, 12.0, 25)
        self.createConsumables(position, 4, 16)

        position = Vec3(-98.0, -52.8, 23)
        self.createConsumables(position, 4, 17)

        position = Vec3(-84.1, -52.8, 23)
        self.createConsumables(position, 4, 18)

        what = 0

        x = -122.4
        y = -52.3
        z = 2

        io = 0

        for i in range(7):

            io += 1
            position = Vec3(x, y, z)
            self.createConsumables(position, 1, io)
            x -= 9

        for i in range(12):

            io += 1
            position = Vec3(x, y, z)
            self.createConsumables(position, 1, io)
            y += 9

        for i in range(12):

            io += 1
            position = Vec3(x, y, z)
            self.createConsumables(position, 1, io)
            x += 9

        x = -91
        y = 29
        z = 64

        for i in range(8):

            io += 1
            position = Vec3(x, y, z)
            self.createConsumables(position, 1, io)
            y -= 9

        for i in range(9):

            io += 1
            position = Vec3(x, y, z)
            self.createConsumables(position, 1, io)
            x -= 9

        for i in range(9):

            io += 1
            position = Vec3(x, y, z)
            self.createConsumables(position, 1, io)
            y += 9

        #PoweUps

        position = Vec3(-315, -9, 85)
        self.createConsumables(position, 7, 1)

        position = Vec3(-90.8, -52.8, 24)
        self.createConsumables(position, 7, 2)

        position = Vec3(-36.2, -95, 5)
        self.createConsumables(position, 6, 1)

        position = Vec3(-251.45, 3.8, 25)
        self.createConsumables(position, 5, 1)

    def doExit(self):
        self.cleanup()
        sys.exit(1)

    def doReset(self):
        self.cleanup()
        self.setup()

    def toggleDebug(self):
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

    def doJump(self):

        speed = 10

        if self.charState['powerdUpJump']:
            speed = 25

        self.character.setJumpSpeed(speed)

        if self.character.isOnGround():
            self.actorNP.play('jump')
            self.character.doJump()
            self.playSfx(self.jumpSound, interrupt = 0, volume = self.volume)

    def soundAndMusicLoader(self):
        self.jumpSound = self.loadSfx('audio/sounds/robot-jump.wav')
        self.landSound = self.loadSfx('audio/sounds/robot-land.wav')
        self.walkSound = self.loadSfx('audio/sounds/robot-step.wav')
        self.damageSound = self.loadSfx('audio/sounds/robot-damage.wav')

        self.levelIntroMusic = self.loadMusic('audio/music/level-1-intro.mp3')
        self.levelLoopMusic = self.loadMusic('audio/music/level-1.mp3')
        self.gameOverMusic = self.loadMusic('audio/music/game-over.mp3')

    def processInput(self, dt):

        movementInput = False

        speed = Vec3(0, 0, 0)
        omega = 0.0
        omegamult = 1.0

        runSpeed = 10

        if self.charState['powerdUpSpeed']:
            runSpeed = 20
            omegamult = 2.0

        if inputState.isSet('forward'):
            speed.setY(runSpeed)
            movementInput = True

        if inputState.isSet('reverse'):
            speed.setY(-runSpeed)
            movementInput = True

        if inputState.isSet('left'):
            speed.setX(-runSpeed)
            movementInput = True

        if inputState.isSet('right'):
            speed.setX(runSpeed)
            movementInput = True

        if inputState.isSet('turnLeft'):
            omega = 120.0 * omegamult
            movementInput = True

        if inputState.isSet('turnRight'):
            omega = -120.0 * omegamult
            movementInput = True

        running = self.actorNP.getAnimControl('run').isPlaying()
        idle = self.actorNP.getAnimControl('idle').isPlaying()
        landing = self.actorNP.getAnimControl('land').isPlaying()
        jumping = self.actorNP.getAnimControl('jump').isPlaying()
        onGround = self.character.isOnGround()

        if movementInput and onGround and not landing:
            self.playSfx(self.walkSound, interrupt = 0, volume = self.volume / 4)

        if movementInput and not landing and not running and not jumping and onGround:
            self.actorNP.loop('run')
        elif not movementInput and not landing and not idle and not jumping and onGround:
            self.actorNP.loop('idle')
        elif not onGround and not landing and not jumping:
            self.actorNP.pose('land', 1)

        self.character.setAngularMovement(omega)
        self.character.setLinearMovement(speed, True)

        # Camera

        startpos = self.characterNP.getPos()

        if inputState.isSet('camLeft'):
            base.camera.setX(base.camera, -25 * globalClock.getDt())
        if inputState.isSet('camRight'):
            base.camera.setX(base.camera, +25 * globalClock.getDt())
        if inputState.isSet('camDown'):
            base.camera.setZ(base.camera, -50 * globalClock.getDt())
        if inputState.isSet('camUp'):
            base.camera.setZ(base.camera, +50 * globalClock.getDt())

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = startpos - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 30.0):
            base.camera.setPos(base.camera.getPos() + camvec * (camdist - 30))
            camdist = 30.0
        if (camdist < 15.0):
            base.camera.setPos(base.camera.getPos() - camvec * (15 - camdist))
            camdist = 15.0


        self.floater.setPos(self.characterNP.getPos())
        self.floater.setZ(self.characterNP.getZ() + 2.0)
        base.camera.lookAt(self.floater)

    def update(self, task):

        # if gameovertrue white out screen and print game over
        # do that tommorow and level design

        if self.characterNP.getPos().getZ() < -50:
            self.healthBar['value'] -= 25
            self.charState['health'] -= 25
            self.charState['powerdUpSpeed'] = False
            self.charState['endOfPowerUpJump'] = False
            self.characterNP.setPos(self.charState['RespawnPos'])


        if self.levelIntroMusic.status() != self.levelIntroMusic.PLAYING and \
            self.levelLoopMusic.status() != self.levelIntroMusic.PLAYING and not self.charState['gameOver']:

            self.playMusic(self.levelLoopMusic, looping = 1, volume=self.volume / 4)

        dt = globalClock.getDt()


        maxTime = 180 + self.charState['bonusTime']

        currentTime = trunc(globalClock.getFrameTime())

        self.levelTime = maxTime - currentTime


        warningMusicRate = 60
        criticalMusicRate = 30

        if self.levelTime <= 0 and self.levelLoopMusic.status() == self.levelLoopMusic.PLAYING:

            self.charState['gameOver'] = True
            # time up display
            self.t.setText('Time Up!')
            self.t.setScale(.04)

            self.levelLoopMusic.stop()
            self.playMusic(self.gameOverMusic, looping=0, volume=self.volume / 4)

            self.popUps['gameOver'].start()
        elif self.charState['health'] <= 0 and self.levelLoopMusic.status() == self.levelLoopMusic.PLAYING:

            self.charState['gameOver'] = True

            self.levelLoopMusic.stop()
            self.playMusic(self.gameOverMusic, looping=0, volume=self.volume / 4)

            self.popUps['gameOver'].start()
        elif self.levelTime > 0 and not self.charState['gameOver']:
            # time display
            self.t.setText(str(self.levelTime))

        if self.levelTime <= warningMusicRate and self.levelTime > criticalMusicRate and not self.charState['gameOver']:
            self.levelLoopMusic.setPlayRate(1.25)
        elif self.levelTime <= criticalMusicRate and not self.charState['gameOver']:
            self.levelLoopMusic.setPlayRate(1.5)
        elif not self.charState['gameOver']:
            self.levelLoopMusic.setPlayRate(1)
            self.charState['gameDuration'] = currentTime

        if self.charState['powerdUpSpeed'] and self.charState['powerdUpJump']:
            self.p.setText('S/J')
            self.actorNP.setColorScale(1.0, 1.0, 0.2, 1.0)
        elif self.charState['powerdUpSpeed']:
            self.p.setText(' S ')
            self.actorNP.setColorScale(1.0, .3, .3, 1.0)
        elif self.charState['powerdUpJump']:
            self.p.setText(' J ')
            self.actorNP.setColorScale(0.3, 0.3, 1.0, 1.0)
        else:
            self.p.setText(' - ')
            self.actorNP.setColorScale(self.charState['defaultColorScale'])

        # used for level building
        self.cx.setText('X: ' + str(self.characterNP.getX()))
        self.cy.setText('Y: ' + str(self.characterNP.getY()))
        self.cz.setText('Z: ' + str(self.characterNP.getZ()))

        if not self.charState['gameOver']:
            self.processInput(dt)
        else:
            self.floater.setPos(self.characterNP.getPos())
            self.floater.setZ(self.characterNP.getZ() + 2.0)
            base.camera.lookAt(self.floater)

        wasOnGround = self.character.isOnGround()

        self.world.doPhysics(dt, 4, 1./240.)
        self.processConsumableContacts()

        isOnGround = self.character.isOnGround()

        if isOnGround and not wasOnGround:
            self.actorNP.play('land')
            self.playSfx(self.landSound, interrupt = 0, volume = self.volume)

        if currentTime > self.charState['endOfPowerUpJump']:
            self.charState['powerdUpJump'] = False

        if currentTime > self.charState['endOfPowerUpSpeed']:
            self.charState['powerdUpSpeed'] = False

        return task.cont

    def cleanup(self):
        self.world = None
        self.render.removeNode()

    def setupLights(self):
        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alightNP = render.attachNewNode(alight)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = render.attachNewNode(dlight)

        self.render.clearLight()
        self.render.setLight(alightNP)
        self.render.setLight(dlightNP)

    def keepSpin(self, task):

        for node, powerUp in self.consumables:
            pass

        return task.cont

    def createFloatingRectangle(self, size, position, name, hpr = LVecBase3f(0,0,0)):

        sizeX = size.getX()
        sizeY = size.getY()
        sizeZ = size.getZ()

        shape = BulletBoxShape(size)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        floorNP.node().addShape(shape)
        # friction does not seem to do anything for BulletCharacterNode
        # floorNP.node().setFriction(50.0)
        floorNP.setPos(position)
        floorNP.setHpr(hpr)

        floorNP.setCollideMask(BitMask32.allOn())

        floorNPModel = loader.loadModel('models/EnvBuildingBlocks/stone-cube/stone.egg')
        floorNPModel.reparentTo(floorNP)
        floorNPModel.setScale(size * 2)
        floorNPModel.setPos(0, 0, -sizeZ)

        self.world.attachRigidBody(floorNP.node())

    def createRotatingRectangle(self, size, position, name, mass = 1000):

        sizeX = size.getX()
        sizeY = size.getY()
        sizeZ = size.getZ()

        shape = BulletBoxShape(size)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        floorNP.node().addShape(shape)
        floorNP.node().setMass(mass)
        floorNP.node().setAngularVelocity(5)
        floorNP.setPos(position)


        floorNP.setCollideMask(BitMask32.allOn())

        floorNPModel = loader.loadModel('models/box.egg')
        floorNPModel.reparentTo(floorNP)
        floorNPModel.setScale(size * 2)
        floorNPModel.setPos(-sizeX, -sizeY, -sizeZ)

        self.world.attachRigidBody(floorNP.node())

        # Hinge
        pivot =  Point3(0, 0, 0)
        axis = Vec3(0, 0, 1)

        hinge = BulletHingeConstraint(floorNP.node(), pivot, axis, True)
        hinge.setDebugDrawSize(4.0)
        hinge.setLimit(0, 360, softness=0.9, bias=0.3, relaxation=1.0)
        self.world.attachConstraint(hinge)

        self.rectangle = floorNP.node()

    def createConsumables(self, position, powerUp, i):

        skin = self.loader.loadModel("models/EnvBuildingBlocks/sphere/ball.egg")

        if powerUp == -1:
            node = BulletGhostNode('Level-End')
            skin.setColorScale(0.2, 0.2, 0.2, 0.5)
            radius = 10

        if powerUp == 0:
            node = BulletGhostNode('wayPoint - ' + str(i))
            radius = 3

        if powerUp == 1:
            node = BulletGhostNode('time + 5 coin(' + str(i) + ')')
            skin.setColorScale(.5, 1.0, .5, 1.0)
            radius = 1

        elif powerUp == 2:
            node = BulletGhostNode('time + 15 coin(' + str(i) + ')')
            skin.setColorScale(.2, 1.0, .2, 1.0)
            radius = 1.5

        elif powerUp == 3:
            node = BulletGhostNode('time - 5 coin(' + str(i) + ')')
            skin.setColorScale(1.0, .5, .5, 1.0)
            radius = 1

        elif powerUp == 4:
            node = BulletGhostNode('time - 15 coin(' + str(i) + ')')
            skin.setColorScale(1.0, .2, .2, 1.0)
            radius = 1.5

        elif powerUp == 5:
            node = BulletGhostNode('high jump power-up(' + str(i) + ')')
            skin.setColorScale(0.3, 0.3, 1.0, 1.0)
            radius = 2

        elif powerUp == 6:
            node = BulletGhostNode('high speed power-up(' + str(i) + ')')
            skin.setColorScale(1.0, 0.0, .5, 1.0)
            radius = 2

        elif powerUp == 7:
            node = BulletGhostNode('high speed and jump power-up(' + str(i) + ')')
            skin.setColorScale(1.0, 1.0, 0.2, 1.0)
            radius = 2

        shape = BulletSphereShape(radius)
        node.addShape(shape)

        np = self.render.attachNewNode(node)
        np.setCollideMask(BitMask32.allOff())
        np.setPos(position)

        skin.reparentTo(np)
        skin.setScale(radius)

        self.world.attachGhost(node)
        self.consumables.append((node, powerUp))

    def processConsumableContacts(self):
        for node, powerUp in self.consumables:
            self.contactWithGhosts(node, powerUp)
        for node, powerUp in self.removeConsumables:

            self.consumables.remove((node, powerUp))
            node.removeAllChildren()
            self.world.remove(node)

        self.removeConsumables = []

    def contactWithGhosts(self, secondNode, powerUp):
        # test sphere for contacts with secondNode
        contactResult = self.world.contactTestPair(self.character, secondNode)  # returns a BulletContactResult object

        if len(contactResult.getContacts()) > 0:

            if powerUp == -1:
                self.charState['levelFinished'] = True
                self.popUps['levelFinished'].start()
            if powerUp == 0:
                self.charState['RespawnPos'] = secondNode.getTransform().getPos()
                self.popUps['wayPoint'].start()
            if powerUp == 1:
                self.charState['bonusTime'] += 5
                self.popUps['+5'].start()
            if powerUp == 2:
                self.charState['bonusTime'] += 15
                self.popUps['+15'].start()
            if powerUp == 3:
                self.charState['bonusTime'] -= 5
                self.popUps['-5'].start()
            if powerUp == 4:
                self.charState['bonusTime'] -= 15
                self.popUps['-15'].start()
            if powerUp == 5:

                if self.charState['powerdUpJump']:
                    self.charState['endOfPowerUpJump'] += 30
                else:
                    self.charState['powerdUpJump'] = True
                    self.charState['endOfPowerUpJump'] = int(globalClock.getFrameTime() + 30)

                self.popUps['Jump'].start()

            if powerUp == 6:

                if self.charState['powerdUpSpeed']:
                    self.charState['endOfPowerUpSpeed'] += 30
                else:
                    self.charState['powerdUpSpeed'] = True
                    self.charState['endOfPowerUpSpeed'] = int(globalClock.getFrameTime() + 30)

                self.popUps['Speed'].start()

            if powerUp == 7:

                if self.charState['powerdUpJump']:
                    self.charState['endOfPowerUpJump'] += 30
                else:
                    self.charState['powerdUpJump'] = True
                    self.charState['endOfPowerUpJump'] = int(globalClock.getFrameTime() + 30)

                if self.charState['powerdUpSpeed']:
                    self.charState['endOfPowerUpSpeed'] += 30
                else:
                    self.charState['powerdUpSpeed'] = True
                    self.charState['endOfPowerUpSpeed'] = int(globalClock.getFrameTime() + 30)

                self.popUps['SpeedAndJump'].start()

            self.removeConsumables.append((secondNode, powerUp))
            print "robot is in contact with: ", secondNode.getName()

    def setup(self):

        # World

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

        self.soundAndMusicLoader()

        self.consumables = []
        self.removeConsumables = []

        self.makeBall()
        self.makePlayer()

        self.playMusic(self.levelIntroMusic, volume=self.volume / 4)

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        base.camera.setPos(self.characterNP.getX() + 5, self.characterNP.getY() + 5, self.characterNP.getZ() + 20)
        base.camera.setHpr(self.characterNP.getHpr())
        base.camera.lookAt(self.floater)

        self.buildLevel()
        self.addItems()
        self.setupGui()

    def setupGui(self):

        y = 1
        x = 1366 / 768.0

        ui = OnscreenImage(image='images/gui.png', pos=(0, 0, 0), scale=(x, y, 1))
        ui.setTransparency(TransparencyAttrib.MAlpha)
        ui.reparentTo(aspect2d)

        self.healthBar = DirectWaitBar(frameSize=(-x / 3.59, x / 3.59, -y / 32.0, y / 30.0),
                                       text="Roby", value=100, range=100, pos=(-.15, 0, -.926))

        self.t = OnscreenText('', pos=(-0.1, 0.916), scale=.1)
        self.p = OnscreenText('', pos=(.97, -.952), scale=.09)

        gameOverImage = OnscreenImage(image='images/game-over.png', pos=(0, 0, 0), scale=(x, y, 1))
        gameOverImage.setTransparency(TransparencyAttrib.MAlpha)
        gameOverImage.reparentTo(aspect2d)
        gameOverImage.setColorScale(LVecBase4f(1, 1, 1, 0))

        fadeInGamOverInterval = gameOverImage.colorScaleInterval(4, LVecBase4f(1, 1, 1, 1))

        levelFinished = OnscreenImage(image='images/level-finished.png', pos=(0, 0, 0), scale=(x, y, 1))
        levelFinished.setTransparency(TransparencyAttrib.MAlpha)
        levelFinished.reparentTo(aspect2d)
        levelFinished.setColorScale(LVecBase4f(1, 1, 1, 0))

        fadeInlevelFinishedInterval = levelFinished.colorScaleInterval(4, LVecBase4f(1, 1, 1, 1))

        waypoint = OnscreenImage(image='images/waypoint.png', pos=(0, 0, 0), scale=(x, y, 1))
        waypoint.setTransparency(TransparencyAttrib.MAlpha)
        waypoint.reparentTo(aspect2d)
        waypoint.setColorScale(LVecBase4f(1, 1, 1, 0))
        waypointFadeIn = waypoint.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        waypointFadeOut = waypoint.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        waypointSeq = Sequence(waypointFadeIn, waypointFadeOut)

        plus5 = OnscreenImage(image='images/plus-5.png', pos=(0, 0, 0), scale=(x, y, 1))
        plus5.setTransparency(TransparencyAttrib.MAlpha)
        plus5.reparentTo(aspect2d)
        plus5.setColorScale(LVecBase4f(1, 1, 1, 0))
        plus5FadeIn = plus5.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        plus5FadeOut = plus5.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        plus5Seq = Sequence(plus5FadeIn, plus5FadeOut)

        plus15 = OnscreenImage(image='images/plus-15.png', pos=(0, 0, 0), scale=(x, y, 1))
        plus15.setTransparency(TransparencyAttrib.MAlpha)
        plus15.reparentTo(aspect2d)
        plus15.setColorScale(LVecBase4f(1, 1, 1, 0))
        plus15FadeIn = plus15.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        plus15FadeOut = plus15.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        plus15Seq = Sequence(plus15FadeIn, plus15FadeOut)

        minus5 = OnscreenImage(image='images/minus-5.png', pos=(0, 0, 0), scale=(x, y, 1))
        minus5.setTransparency(TransparencyAttrib.MAlpha)
        minus5.reparentTo(aspect2d)
        minus5.setColorScale(LVecBase4f(1, 1, 1, 0))
        minus5FadeIn = minus5.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        minus5FadeOut = minus5.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        minus5Seq = Sequence(minus5FadeIn, minus5FadeOut)

        minus15 = OnscreenImage(image='images/minus-15.png', pos=(0, 0, 0), scale=(x, y, 1))
        minus15.setTransparency(TransparencyAttrib.MAlpha)
        minus15.reparentTo(aspect2d)
        minus15.setColorScale(LVecBase4f(1, 1, 1, 0))
        minus15FadeIn = minus15.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        minus15FadeOut = minus15.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        minus15Seq = Sequence(minus15FadeIn, minus15FadeOut)

        jumpBoost = OnscreenImage(image='images/jump-boost.png', pos=(0, 0, 0), scale=(x, y, 1))
        jumpBoost.setTransparency(TransparencyAttrib.MAlpha)
        jumpBoost.reparentTo(aspect2d)
        jumpBoost.setColorScale(LVecBase4f(1, 1, 1, 0))
        jumpBoostFadeIn = jumpBoost.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        jumpBoostFadeOut = jumpBoost.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        jumpBoostSeq = Sequence(jumpBoostFadeIn, jumpBoostFadeOut)

        speedBoost = OnscreenImage(image='images/speed-boost.png', pos=(0, 0, 0), scale=(x, y, 1))
        speedBoost.setTransparency(TransparencyAttrib.MAlpha)
        speedBoost.reparentTo(aspect2d)
        speedBoost.setColorScale(LVecBase4f(1, 1, 1, 0))
        speedBoostFadeIn = speedBoost.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        speedBoostFadeOut = speedBoost.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        speedBoostSeq = Sequence(speedBoostFadeIn, speedBoostFadeOut)

        superBoost = OnscreenImage(image='images/super-boost.png', pos=(0, 0, 0), scale=(x, y, 1))
        superBoost.setTransparency(TransparencyAttrib.MAlpha)
        superBoost.reparentTo(aspect2d)
        superBoost.setColorScale(LVecBase4f(1, 1, 1, 0))
        superBoostFadeIn = superBoost.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        superBoostFadeOut = superBoost.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        superBoostSeq = Sequence(superBoostFadeIn, superBoostFadeOut)




        self.popUps = {'+5': plus5Seq, '+15': plus15Seq, '-5': minus5Seq, '-15': minus15Seq, 'Jump': jumpBoostSeq,
                       'Speed': speedBoostSeq, 'SpeedAndJump': superBoostSeq, 'wayPoint': waypointSeq, 'gameOver': fadeInGamOverInterval,
                       'levelFinished': fadeInlevelFinishedInterval}

    def makePlayer(self):
        # Character
        h = 6.5
        w = 1.3
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        self.characterNP = self.render.attachNewNode(self.character)

        what = 0

        self.characterNP.setPos(200, 0, 5)

        self.characterNP.setH(45)
        print self.character.getMaxSlope()
        # does nothing for slipage
        # self.character.setMaxSlope(89.0)
        self.characterNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.character)

        self.actorNP = Actor('models/robot/lack.egg', {
            'idle': 'models/robot/lack-idle.egg',
            'run': 'models/robot/lack-run.egg',
            'jump': 'models/robot/lack-jump.egg',
            'land': 'models/robot/lack-land.egg',
            'tightrope': 'models/robot/lack-tightrope.egg',
            'damage': 'models/robot/lack-damage.egg'})

        self.actorNP.reparentTo(self.characterNP)
        self.actorNP.setScale(0.3048)
        self.actorNP.setH(180)
        self.actorNP.setPos(0, 0, .45)

        self.charState = {'health': 100, 'bonusTime': 0, 'RespawnPos': self.characterNP.getPos(),'gameOver': False, 'levelFinished': False, 'gameDuration': 0, 'defaultColorScale': self.actorNP.getColorScale(),
                          'powerdUpJump': False, 'endOfPowerUpJump': 0, 'powerdUpSpeed': False, 'endOfPowerUpSpeed': 0}

    def makeBall(self):
        # Sphere
        shape = BulletSphereShape(.25)
        node = BulletRigidBodyNode('Ball')
        node.setMass(.2)
        node.addShape(shape)

        # attach
        self.sphere = self.render.attachNewNode(node)
        self.sphere.setPos(-122, 0, 6)
        self.world.attachRigidBody(node)

        # attached object image to physics
        smileyFace = self.loader.loadModel("models/smiley")
        smileyFace.reparentTo(self.sphere)
        smileyFace.setScale(.25)

game = CharacterController()
game.run()
