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




        # used in debug mode
        self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
        self.cx = onscreenText(.90, '')
        self.cy = onscreenText(.85, '')
        self.cz = onscreenText(.80, '')

        self.debugNP.hide()
        self.cx.hide()
        self.cy.hide()
        self.cz.hide()

        self.volume = .5
        self.setupLights()
        self.setup()

        # Input
        self.accept('escape', self.doExit)
        # self.accept('r', self.doReset)
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

        inputState.watchWithModifiers('helpMenu', 'f1')

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
        position = Vec3(-135, 60, 72)
        self.createFloatingRectangle(size, position, 'P2.5')

        size = Vec3(3, 3, 1)
        position = Vec3(-119, 60, 78)
        self.createFloatingRectangle(size, position, 'P2.6')

        size = Vec3(3, 3, 1)
        position = Vec3(-135, 60, 84)
        self.createFloatingRectangle(size, position, 'P2.7')

        size = Vec3(3, 3, 1)
        position = Vec3(-119, 60, 90)
        self.createFloatingRectangle(size, position, 'P2.8')

        size = Vec3(3, 3, 1)
        position = Vec3(-90, -8, 95)
        self.createFloatingRectangle(size, position, 'P2.9')

        size = Vec3(3, 3, 1)
        position = Vec3(-70, -8, 101)
        self.createFloatingRectangle(size, position, 'P2.10')

        size = Vec3(3, 3, 1)
        position = Vec3(-85, 10, 106)
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

        p1 = self.createFloatingRectangle(size, position, 'P3.1')

        size = Vec3(3, 3, 1)
        position = Vec3(-209, -6, 105)

        p2 = self.createFloatingRectangle(size, position, 'P3.2')

        size = Vec3(3, 3, 1)
        position = Vec3(-238, 6, 105)

        p3 = self.createFloatingRectangle(size, position, 'P3.3')

        size = Vec3(3, 3, 1)
        position = Vec3(-238, -18, 105)

        p4 = self.createFloatingRectangle(size, position, 'P3.4')

        size = Vec3(3, 3, 1)
        position = Vec3(-267, -30, 105)

        p5 = self.createFloatingRectangle(size, position, 'P3.5')

        size = Vec3(3, 3, 1)
        position = Vec3(-267, 18, 105)

        p6 = self.createFloatingRectangle(size, position, 'P3.6')


        # button variables
        position = Vec3(-130, -14, 107)
        platforms =[p1, p2, p3, p4, p5, p6]
        time = 30
        name = 'Button1'
        buttonType = 3

        self.createButtonWithPlatformAction(position, platforms, time, name, buttonType)

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

        for i in range(12):

            io += 1
            position = Vec3(x, y, z)
            self.createConsumables(position, 3, io)
            y -= 9

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

        for i in range(10):

            io += 1
            position = Vec3(x, y, z)
            self.createConsumables(position, 3, io)
            x += 9

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
            self.cx.show()
            self.cy.show()
            self.cz.show()
        else:
            self.debugNP.hide()
            self.cx.hide()
            self.cy.hide()
            self.cz.hide()

    def doJump(self):

        speed = 10

        if self.charState['powerdUpJump']:
            speed = 25

        self.character.setJumpSpeed(speed)

        if self.character.isOnGround():
            self.actorNP.play('jump')
            self.character.doJump()
            self.playSfx(self.jumpSound, interrupt=0, volume=self.volume * 2)

    def soundAndMusicLoader(self):
        self.jumpSound = self.loadSfx('audio/sounds/robot-jump.wav')
        self.landSound = self.loadSfx('audio/sounds/robot-land.wav')
        self.walkSound = self.loadSfx('audio/sounds/robot-step.wav')
        self.damageSound = self.loadSfx('audio/sounds/robot-damage.wav')

        self.waypointSound = self.loadSfx('audio/sounds/waypoint.wav')

        self.onOffSound = self.loadSfx('audio/sounds/on-off.wav')
        self.tickTockSound = self.loadSfx('audio/sounds/tick-tock-1.wav')

        self.plus5Sound = self.loadSfx('audio/sounds/plus-5.wav')
        self.plus15Sound = self.loadSfx('audio/sounds/plus-15.wav')
        self.minus5Sound = self.loadSfx('audio/sounds/minus-5.wav')
        self.minus15Sound = self.loadSfx('audio/sounds/minus-15.wav')
        self.boostSound = self.loadSfx('audio/sounds/boosts.wav')




        self.levelIntroMusic = self.loadMusic('audio/music/level-1-intro.mp3')
        self.levelLoopMusic = self.loadMusic('audio/music/level-1.mp3')
        self.gameOverMusic = self.loadMusic('audio/music/game-over.mp3')
        self.levelComplete = self.loadMusic('audio/music/complete.mp3')

    def processInput(self, dt):

        movementInput = False

        speed = Vec3(0, 0, 0)
        omega = 0.0
        omegamult = 1.0

        runSpeed = 10

        if inputState.isSet('helpMenu'):
            self.helpMenu.show()
        else:
            self.helpMenu.hide()

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
            self.playSfx(self.walkSound, interrupt=0, volume=self.volume / 3)

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

        if abs(base.camera.getZ() - self.characterNP.getZ()) > 30.0:
            base.camera.setZ(self.characterNP.getZ() + 30)

        self.floater.setPos(self.characterNP.getPos())
        self.floater.setZ(self.characterNP.getZ() + 2.0)
        base.camera.lookAt(self.floater)

    def update(self, task):

        if self.characterNP.getPos().getZ() < -50:
            self.healthBar['value'] -= 25
            self.charState['health'] -= 25
            self.charState['powerdUpSpeed'] = False
            self.charState['endOfPowerUpJump'] = False
            self.characterNP.setPos(self.charState['RespawnPos'])

        if self.levelIntroMusic.status() != self.levelIntroMusic.PLAYING and \
                        self.levelLoopMusic.status() != self.levelLoopMusic.PLAYING and not self.charState['gameOver']\
                and not self.charState['levelFinished']:
            self.playMusic(self.levelLoopMusic, looping=1, volume=self.volume / 4)

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
        elif self.levelTime > 0 and not self.charState['gameOver'] and not self.charState['levelFinished']:
            # time display
            self.t.setText(str(self.levelTime))

        if self.levelTime <= warningMusicRate and self.levelTime > criticalMusicRate and not self.charState['gameOver']:
            self.levelLoopMusic.setPlayRate(1.25)
        elif self.levelTime <= criticalMusicRate and not self.charState['gameOver']:
            self.levelLoopMusic.setPlayRate(1.5)
        elif not self.charState['gameOver'] and not self.charState['levelFinished']:
            self.levelLoopMusic.setPlayRate(1)
            self.charState['gameScore'] = currentTime

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

        self.world.doPhysics(dt, 4, 1. / 240.)
        self.processConsumableContacts()
        self.processButtonContacts()

        isOnGround = self.character.isOnGround()

        if isOnGround and not wasOnGround:
            self.actorNP.play('land')
            self.playSfx(self.landSound, interrupt=0, volume=self.volume * 2)

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

        # sun right above
        # Vec3(0, -90, 0)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = render.attachNewNode(dlight)

        self.render.clearLight()
        self.render.setLight(alightNP)
        self.render.setLight(dlightNP)

    def createFloatingRectangle(self, size, position, name, hpr=LVecBase3f(0, 0, 0)):

        sizeX = size.getX()
        sizeY = size.getY()
        sizeZ = size.getZ()

        shape = BulletBoxShape(size)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        floorNP.node().addShape(shape)
        floorNP.setPos(position)
        floorNP.setHpr(hpr)

        floorNP.setCollideMask(BitMask32.allOn())
        floorNPModel = loader.loadModel('models/EnvBuildingBlocks/stone-cube/stone.egg')
        # floorNPModel = loader.loadModel('models/EnvBuildingBlocks/brick-cube/brick.egg')


        # change texture of model

        # tex = loader.loadTexture('models/EnvBuildingBlocks/stone-cube/stone.png')
        # tex.setWrapU(Texture.WMRepeat)
        # tex.setWrapV(Texture.WMRepeat)
        # floorNPModel.setTexture(tex, 1)


        floorNPModel.reparentTo(floorNP)
        # floorNPModel.setScale(1)
        floorNPModel.setScale(size * 2)
        floorNPModel.setPos(0, 0, -sizeZ)

        self.world.attachRigidBody(floorNP.node())

        return floorNP

    # create a button at position that performs action on platforms
    # type 0: platforms appear for a period of time, button vanishes for same period
    # type 1: platforms vanish for a period of time, button vanishes for same period
    # type 2: platforms vanish indefinetly along with button
    # type 3: platforms appear indefinetly , button vanishes button

    def createButtonWithPlatformAction(self, position, platforms, time, name, buttonType=0):

        switchAction = self.makeSwitchSequencePlatforms(platforms, time, buttonType)

        button, buttonAction = self.makeSwitch(position, time, name, buttonType)

        self.buttonsWithSequences.append({'button': button, 'buttonAction': buttonAction,
                                          'switchAction': switchAction, 'buttonType': buttonType, 'time': time})

    # ::: helper functions for createButtonWithPlatformAction :::

    def platformsAppear(self, skins, platformNPs):

        for i in range(len(platformNPs)):
            platformNPs[i].node().addChild(skins[i])
            platformNPs[i].node().setCollisionResponse(True)

    def platformsVanish(self, platformNPs):

        for i in range(len(platformNPs)):
            platformNPs[i].node().removeAllChildren()
            platformNPs[i].node().setCollisionResponse(False)

    def makeSwitchSequencePlatforms(self, platformNPs, countdown, buttonType=0):

        listchild = []

        for platformNP in platformNPs:
            listchild.append(platformNP.node().getChild(0))

        appear = Func(self.platformsAppear, listchild, platformNPs)
        vanish = Func(self.platformsVanish, platformNPs)
        delay = Wait(countdown)

        if buttonType == 0:

            self.platformsVanish(platformNPs)
            return Sequence(appear, delay, vanish)

        elif buttonType == 1:

            return Sequence(vanish, delay, appear)

        elif buttonType == 2:

            return Sequence(vanish)

        elif buttonType == 3:

            self.platformsVanish(platformNPs)

            return Sequence(appear)

        else:

            return False

    def playButtonCountdown(self, countdown, buttonType):

        half = countdown / 2.0
        quarter = half / 2.0

        speedUpDelay1 = Wait(half)
        speedUpDelay2 = Wait(quarter)

        speedUp1 = Func(self.tickTockSound.setPlayRate, 1.20)
        speedUp2 = Func(self.tickTockSound.setPlayRate, 1.5)
        stopclock = Func(self.tickTockSound.stop)

        self.onOffSound.setVolume(self.volume)
        self.tickTockSound.setPlayRate(1)
        self.tickTockSound.setLoop(True)

        onOffSound = Func(self.onOffSound.play)
        tickTock = Func(self.tickTockSound.play)

        if buttonType == 0 or buttonType == 1:

            Sequence(onOffSound, tickTock, speedUpDelay1, speedUp1, speedUpDelay2, speedUp2,
                     speedUpDelay2, stopclock, onOffSound).start()
        elif buttonType == 2 or buttonType == 3:
            Sequence(onOffSound).start()

    def makeSwitch(self, pos, countdown, name, buttonType=0):

        posButton = pos + Vec3(0, 0, .5)
        size1 = Vec3(1, 1, .25)
        size2 = Vec3(2, 2, .25)

        button = self.createFloatingRectangle(size1, posButton, name)
        self.createFloatingRectangle(size2, pos, name + ' - Base')

        platformNPs = [button]
        listchild = [button.node().getChild(0)]

        vanish = Func(self.platformsVanish, platformNPs)
        appear = Func(self.platformsAppear, listchild, platformNPs)
        delay = Wait(countdown)

        if buttonType == 0 or buttonType == 1:
            button.setColorScale(0.2, 1.0, 0.2, 1)
            return button, Sequence(vanish, delay, appear)
        elif buttonType == 2 or buttonType == 3:
            button.setColorScale(1.0, 0.2, 0.2, 1)
            return button, Sequence(vanish)
        else:
            return False

    # used to process button actions on contact
    def processButtonContacts(self):
        for item in self.buttonsWithSequences:
            self.contactWithButtons(item)
        for item in self.removeButtons:
            self.buttonsWithSequences.remove(item)
            item['button'].node().removeAllChildren()
            self.world.remove(item['button'].node())

        self.removeButtons = []

    # ::: helper function for processButtonContacts :::

    def contactWithButtons(self, buttonDict):

        secondNode = buttonDict['button'].node()
        buttonType = buttonDict['buttonType']

        contactResult = self.world.contactTestPair(self.character, secondNode)  # returns a BulletContactResult object

        if len(contactResult.getContacts()) > 0 and (buttonType == 0 or buttonType == 1) and \
                not buttonDict['buttonAction'].isPlaying():
            self.playButtonCountdown(buttonDict['time'], buttonType)
            buttonDict['buttonAction'].start()
            buttonDict['switchAction'].start()

            print "activated : ", secondNode.getName()

        if len(contactResult.getContacts()) > 0 and (buttonType == 2 or buttonType == 3):
            self.playButtonCountdown(buttonDict['time'], buttonType)
            buttonDict['buttonAction'].start()
            buttonDict['switchAction'].start()
            self.removeButtons.append(buttonDict)

            print "activated : ", secondNode.getName()

    # creates consumable items, waypoints, and timewarp(end of level)
    # i: the number to append to the name for type of consumable
    # powerUp -1: creates timewarp
    # powerUp 0: creates waypoint
    # powerUp 1: creates +5 time consumable
    # powerUp 2: creates +15 time consumable
    # powerUp 3: creates -5 time consumable
    # powerUp 4: creates -15 time consumable
    # powerUp 5: creates jump-boost consumable
    # powerUp 6: creates speed-boost consumable
    # powerUp 7: creates super-boost (speed and jump) consumable

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
            self.contactWithConsumables(node, powerUp)
        for node, powerUp in self.removeConsumables:
            self.consumables.remove((node, powerUp))
            node.removeAllChildren()
            self.world.remove(node)

        self.removeConsumables = []

    def contactWithConsumables(self, secondNode, powerUp):
        # test sphere for contacts with secondNode
        contactResult = self.world.contactTestPair(self.character, secondNode)  # returns a BulletContactResult object

        if len(contactResult.getContacts()) > 0:

            if powerUp == -1:
                self.charState['levelFinished'] = True
                self.popUps['levelFinished'].start()
                self.levelLoopMusic.stop()
                self.playMusic(self.levelComplete, looping=1, volume=self.volume / 4)

            if powerUp == 0:
                self.charState['RespawnPos'] = secondNode.getTransform().getPos()
                self.popUps['wayPoint'].start()
                self.waypointSound.play()

            if powerUp == 1:
                self.charState['bonusTime'] += 5
                self.popUps['+5'].start()
                self.plus5Sound.setVolume(self.volume)
                self.plus5Sound.play()
            if powerUp == 2:
                self.charState['bonusTime'] += 15
                self.popUps['+15'].start()
                self.plus15Sound.setVolume(self.volume)
                self.plus15Sound.play()
            if powerUp == 3:
                self.charState['bonusTime'] -= 5
                self.popUps['-5'].start()
                self.minus5Sound.setVolume(self.volume * 2)
                self.minus5Sound.play()
            if powerUp == 4:
                self.charState['bonusTime'] -= 15
                self.popUps['-15'].start()
                self.minus15Sound.setVolume(self.volume * 2)
                self.minus15Sound.play()
            if powerUp == 5:

                if self.charState['powerdUpJump']:
                    self.charState['endOfPowerUpJump'] += 30
                else:
                    self.charState['powerdUpJump'] = True
                    self.charState['endOfPowerUpJump'] = int(globalClock.getFrameTime() + 30)

                self.popUps['Jump'].start()
                self.boostSound.play()

            if powerUp == 6:

                if self.charState['powerdUpSpeed']:
                    self.charState['endOfPowerUpSpeed'] += 30
                else:
                    self.charState['powerdUpSpeed'] = True
                    self.charState['endOfPowerUpSpeed'] = int(globalClock.getFrameTime() + 30)

                self.popUps['Speed'].start()
                self.boostSound.play()

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
                self.boostSound.play()

            self.removeConsumables.append((secondNode, powerUp))
            print "robot is in contact with: ", secondNode.getName()

    def setup(self):

        # World

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

        self.soundAndMusicLoader()

        # holds ghost objects
        self.consumables = []
        self.removeConsumables = []

        # holds dictionary for button actions
        self.buttonsWithSequences = []
        self.removeButtons = []

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        self.buildLevel()
        self.addItems()
        self.setupGui()
        self.makePlayer()

        base.camera.setPos(self.characterNP.getX() + 5, self.characterNP.getY() + 5, self.characterNP.getZ() + 20)
        base.camera.setHpr(self.characterNP.getHpr())
        base.camera.lookAt(self.floater)

        self.playMusic(self.levelIntroMusic, volume=self.volume / 4)
        self.popUps['levelTip'].start()

        self.envBack = loader.loadModel('models/EnvBackgrounds/partlysunny/partlysunny.egg')
        self.envBack.setScale(100)
        self.envBack.reparentTo(render)

        skyPos = self.characterNP.getPos()
        skyPos.setZ(skyPos.getZ() - 1000)
        self.envBack.setPos(skyPos)

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

        levelTip = OnscreenImage(image='images/level-1-tip.png', pos=(0, 0, 0), scale=(x, y, 1))
        levelTip.setTransparency(TransparencyAttrib.MAlpha)
        levelTip.reparentTo(aspect2d)
        levelTip.setColorScale(LVecBase4f(1, 1, 1, 0))
        levelTipFadeIn = levelTip.colorScaleInterval(2, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        levelTipFadeOut = levelTip.colorScaleInterval(3, Vec4(1, 1, 1, 0))

        levelTipSeq = Sequence(levelTipFadeIn, levelTipFadeOut)

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
                       'Speed': speedBoostSeq, 'SpeedAndJump': superBoostSeq, 'wayPoint': waypointSeq,
                       'levelTip': levelTipSeq, 'gameOver': fadeInGamOverInterval,
                       'levelFinished': fadeInlevelFinishedInterval}

        self.createHelpMenu()

    def createHelpMenu(self):

        x =  self.getAspectRatio()

        self.helpMenu = DirectFrame(frameColor=(0, 0, 0, .8), frameSize=(-x, x, 1, -1), pos=(0, 0, 0))

        OnscreenText(parent=self.helpMenu, text='CHARACTER CONTROLS', pos=(-1.0, 0.8), scale=0.1,
                                   fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[w] - Move Forward', pos=(-0.995, 0.6), scale=0.07,
                     fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[a] - Turn Left', pos=(-1.08, 0.5), scale=0.07,
                     fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[d] - Turn Right', pos=(-1.06, 0.4), scale=0.07,
                     fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[s] - Move Backwards', pos=(-0.961, 0.3),
                     scale=0.07, fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[space] - Jump', pos=(-1.06, 0.2), scale=0.07,
                     fg=(255, 255, 255, 1))


        OnscreenText(parent=self.helpMenu, text='CAMERA CONTROLS', pos=(1.0, .8), scale=0.1,
                     fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[up-arrow] - Move Up', pos=(0.951, 0.6), scale=0.07,
                     fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[down-arrow] - Move Down', pos=(1.04, 0.5), scale=0.07,
                     fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[left-arrow] - Rotate Left', pos=(1.0, 0.4), scale=0.07,
                     fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[right-arrow] - Rotate Right', pos=(1.04, 0.3),
                     scale=0.07, fg=(255, 255, 255, 1))

        OnscreenText(parent=self.helpMenu, text='MISC COMMANDS', pos=(0.0, -0.3), scale=0.1,
                     fg=(255, 255, 255, 1))

        OnscreenText(parent=self.helpMenu, text='[F1] - Help Menu', pos=(0.0, -.4), scale=0.07,
                                   fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[F3] - Toggle Debug Mode', pos=(0.16, -.5), scale=0.07,
                     fg=(255, 255, 255, 1))
        OnscreenText(parent=self.helpMenu, text='[esc] - Quit', pos=(-0.07, -.6), scale=0.07,
                     fg=(255, 255, 255, 1))

    def makePlayer(self):
        # Character
        h = 6.5
        w = 1.3
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        self.characterNP = self.render.attachNewNode(self.character)

        # change character spawn position for testing by commenting out current setPos
        # and uncommenting new position below line 1368-1371

        # self.characterNP.setPos(-400, -6, 127)
        # self.characterNP.setPos(-131, 2, 111)
        # self.characterNP.setPos(-40, 0, 5)
        self.characterNP.setPos(200, 0, 25)

        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.character)

        self.actorNP = Actor('models/characters/robot/lack.egg', {
            'idle': 'models/characters/robot/lack-idle.egg',
            'run': 'models/characters/robot/lack-run.egg',
            'jump': 'models/characters/robot/lack-jump.egg',
            'land': 'models/characters/robot/lack-land.egg',
            'tightrope': 'models/characters/robot/lack-tightrope.egg',
            'damage': 'models/characters/robot/lack-damage.egg'})

        self.actorNP.reparentTo(self.characterNP)
        self.actorNP.setScale(0.3048)
        self.actorNP.setH(180)
        self.actorNP.setPos(0, 0, .45)

        self.charState = {'health': 100, 'bonusTime': 0, 'RespawnPos': self.characterNP.getPos(), 'gameOver': False,
                          'levelFinished': False, 'gameScore': 0, 'defaultColorScale': self.actorNP.getColorScale(),
                          'powerdUpJump': False, 'endOfPowerUpJump': 0, 'powerdUpSpeed': False, 'endOfPowerUpSpeed': 0}

game = CharacterController()
game.run()