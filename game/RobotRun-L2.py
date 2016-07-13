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

        size = Vec3(16, 16, 1)
        position = Vec3(200, 0, 0)
        p0 = self.createFloatingRectangle(size, position, 'P1')

        size = Vec3(6, .5, 1)
        position = Vec3(40, 0, 0)
        p1 =self.createFloatingRectangle(size, position, 'P1.1', (-30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(20, 0, 0)
        p2 = self.createFloatingRectangle(size, position, 'P1.2', (30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(0, 0, 0)
        p3 =self.createFloatingRectangle(size, position, 'P1.3', (-30, 0, 0))

        size = Vec3(6, .5, 1)
        position = Vec3(-20, 0, 0)
        p4 = self.createFloatingRectangle(size, position, 'P1.4', (30, 0, 0))

        platforms = [p1,p2,p3,p4]
        time = 10
        position = Vec3(200, 0, 1)
        name = 'SW1'
        buttonType = 3

        self.createButtonWithPlatformAction(position, platforms, time, name, buttonType)

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

        what = 0

        x = -122.4
        y = -52.3
        z = 2

        io = 0

        for i in range(7):

            io += 1
            position = Vec3(x, y, z)
            # self.createConsumables(position, 1, io)
            x -= 9

        for i in range(12):

            io += 1
            position = Vec3(x, y, z)
            # self.createConsumables(position, 1, io)
            y += 9

        for i in range(12):

            io += 1
            position = Vec3(x, y, z)
            # self.createConsumables(position, 1, io)
            x += 9

        x = -91
        y = 29
        z = 64

        for i in range(8):

            io += 1
            position = Vec3(x, y, z)
            # self.createConsumables(position, 1, io)
            y -= 9

        for i in range(9):

            io += 1
            position = Vec3(x, y, z)
            # self.createConsumables(position, 1, io)
            x -= 9

        for i in range(9):

            io += 1
            position = Vec3(x, y, z)
            # self.createConsumables(position, 1, io)
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
            self.playSfx(self.jumpSound, interrupt=0, volume=self.volume)

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
            self.playSfx(self.walkSound, interrupt=0, volume=self.volume / 4)

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
            self.playSfx(self.landSound, interrupt=0, volume=self.volume)

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
        # friction does not seem to do anything for BulletCharacterNode
        # floorNP.node().setFriction(50.0)
        floorNP.setPos(position)
        floorNP.setHpr(hpr)

        floorNP.setCollideMask(BitMask32.allOn())
        floorNPModel = loader.loadModel('models/EnvBuildingBlocks/stone-cube/stone.egg')
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
                self.plus5Sound.play()
            if powerUp == 2:
                self.charState['bonusTime'] += 15
                self.popUps['+15'].start()
                self.plus15Sound.play()
            if powerUp == 3:
                self.charState['bonusTime'] -= 5
                self.popUps['-5'].start()
                self.minus5Sound.play()
            if powerUp == 4:
                self.charState['bonusTime'] -= 15
                self.popUps['-15'].start()
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

    def makePlayer(self):
        # Character
        h = 6.5
        w = 1.3
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        self.characterNP = self.render.attachNewNode(self.character)

        what = 0

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