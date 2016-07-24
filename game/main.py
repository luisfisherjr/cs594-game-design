import sys
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.showbase.InputStateGlobal import inputState
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp
from math import trunc
import random
from panda3d.core import TransparencyAttrib
loadPrcFileData("", "win-size 1366 768")

def onscreenText(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale=.05)

class CharacterController(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.volume = .5

        self.soundAndMusicLoader()

        self.showMainMenu()

        self.playMusic(self.mainMenuMusic, volume=self.volume / 4)

    def showMainMenu(self):

        x = self.getAspectRatio()

        num = random.randint(0, 1)

        if num ==0:

            self.MenuFrame = DirectFrame(image = 'images/screen1.png', image_scale = (x, 1, 1), frameColor=(0, 0, 0, .8),
                                         frameSize=(-x, x, 1, -1), pos=(0, 0, 0))

        elif num == 1:
            self.MenuFrame = DirectFrame(image='images/screen2.png', image_scale=(x, 1, 1), frameColor=(0, 0, 0, .8),
                                         frameSize=(-x, x, 1, -1), pos=(0, 0, 0))

        OnscreenText(parent=self.MenuFrame, text='Running Roby!', pos=(-1.0, 0.8), scale=0.1,
                     fg=(255, 255, 255, 1))

        DirectButton(parent=self.MenuFrame, text=("Level  1 ", "Loading", "Level  1 ", "disabled"),pos=(.5, 0, 0.1), scale=.1,
                         command=self.select1, clickSound=self.onOffSound)

        DirectButton(parent=self.MenuFrame, text=("Level  2 ", "Loading", "Level  2 ", "disabled"),pos=(.5, 0, -0.1),scale=.1,
                                command=self.select2, clickSound=self.onOffSound)

        DirectButton(parent=self.MenuFrame, text=("Exit", "Exit", "Exit", "disabled"),
                                    pos=(.5, 0, -0.3), scale=.1,
                                    command=self.doExit, clickSound=self.onOffSound)

    def select1(self):
        self.setupLevel(1)

    def select2(self):
        self.setupLevel(2)

    def buildStage1(self):

        # holds platforms
        self.movingPlatforms = []
        self.allPlatforms = []

        self.buttonBases = []

        # creates platforms
        self.buildStagePlatforms('data/stage1.txt')

        # Task
        taskMgr.add(self.keepPlatformsMoving, 'movingPlatforms')

    def buildStage2(self):

        # holds platforms
        self.movingPlatforms = []
        self.allPlatforms = []

        self.buttonBases = []

        # creates platforms
        self.buildStagePlatforms('data/stage2.txt')

        # Task
        taskMgr.add(self.keepPlatformsMoving, 'movingPlatforms')

    def buildStagePlatforms(self, stageFile):

        stageInstructions = open(stageFile)

        for line in stageInstructions:

            parameters = line.strip().split(',')

            type = int(parameters[0])

            if type == 0:

                sizeX = float(parameters[1])
                sizeY = float(parameters[2])
                sizeZ = float(parameters[3])

                size = Vec3(sizeX, sizeY, sizeZ)

                posX = float(parameters[4])
                posY = float(parameters[5])
                posZ = float(parameters[6])

                position = Vec3(posX, posY, posZ)

                name = parameters[7]

                h = float(parameters[8])
                p = float(parameters[9])
                r = float(parameters[10])

                hpr = Vec3(h, p, r)

                skin = int(parameters[11])
                floatingPlatform = self.createFloatingRectangle(size, position, name, hpr, skin)

                self.allPlatforms.append(floatingPlatform)

            if type == 1:

                sizeX = float(parameters[1])
                sizeY = float(parameters[2])
                sizeZ = float(parameters[3])

                size = Vec3(sizeX, sizeY, sizeZ)

                posX = float(parameters[4])
                posY = float(parameters[5])
                posZ = float(parameters[6])

                position = Vec3(posX, posY, posZ)

                name = parameters[7]

                h = float(parameters[8])
                p = float(parameters[9])
                r = float(parameters[10])

                hpr = Vec3(h, p, r)

                maxX = float(parameters[11])
                maxY = float(parameters[12])
                maxZ = float(parameters[13])

                maxPos = Vec3(maxX, maxY, maxZ)

                minX = float(parameters[14])
                minY = float(parameters[15])
                minZ = float(parameters[16])

                minPos = Vec3(minX, minY, minZ)

                moveX = float(parameters[17])
                moveY = float(parameters[18])
                moveZ =float(parameters[19])

                pathVector = Vec3(moveX, moveY, moveZ)

                skin = int(parameters[20])
                movingPlatform = self.createMovingRectangle(size, position, name, hpr, maxPos, minPos, pathVector, skin)

                self.allPlatforms.append(movingPlatform)

            if type == 2:

                buttonType = int(parameters[1])

                time = float(parameters[2])

                posX = float(parameters[3])
                posY = float(parameters[4])
                posZ = float(parameters[5])

                position = Vec3(posX, posY, posZ)

                name = parameters[6]

                platforms = []

                print len(parameters)

                for i in range(7, len(parameters)):

                    platforms.append(self.allPlatforms[int(parameters[i])])

                button = self.createButtonWithPlatformAction(position, platforms, time, name, buttonType)

                self.allPlatforms.append(button)

    def addEnemiesStage1(self):

        # holds enemies
        self.allEnemies = []

        #creates enamies
        self.addEnamies('data/enemies1.txt')

        # Task
        taskMgr.add(self.enemyStateChanger, 'enemyType1Task')

    def addEnemiesStage2(self):

        # holds enemies
        self.allEnemies = []

        #creates enamies
        self.addEnamies('data/enemies2.txt')

        # Task
        taskMgr.add(self.enemyStateChanger, 'enemyType1Task')

    def addEnamies(self, enemyFile):

        enemyInstructions = open(enemyFile)

        for line in enemyInstructions:

            parameters = line.strip().split(',')

            type = int(parameters[0])

            if type == 0:

                name = parameters[1]

                anchorX = float(parameters[2])
                anchorY = float(parameters[3])
                anchorZ = float(parameters[4])

                anchorPos = Vec3(anchorX, anchorY, anchorZ)


                radFromAnchor = float(parameters[5])
                maxFromAnchor = float(parameters[6])
                detectionRange = float(parameters[7])
                enemySpeed = float(parameters[8])

                enamy = self.makeEnemy1(name, anchorPos, radFromAnchor, maxFromAnchor, detectionRange, enemySpeed)

                self.allEnemies.append(enamy)

    def addItemsStage1(self):

        # holds enemies
        self.allConsumable = []

        #creates enamies
        self.addItems('data/items1.txt')

    def addItemsStage2(self):

        # holds enemies
        self.allConsumable = []

        #creates enamies
        self.addItems('data/items2.txt')

    def addItems(self, itemFile):

        itemInstructions = open(itemFile)

        for line in itemInstructions:

            parameters = line.strip().split(',')

            type = int(parameters[0])
            number = int(parameters[1])

            posX = float(parameters[2])
            posY = float(parameters[3])
            posZ = float(parameters[4])

            position = Vec3(posX, posY, posZ)

            consumable = self.createConsumables(position, type, number)
            self.allConsumable.append(consumable)

    def doExit(self):
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
            self.playSfx(self.jumpSound, interrupt=0, volume=self.volume)

    def soundAndMusicLoader(self):

        self.levelLoopMusic = None
        self.levelIntroMusic = None

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

        self.mainMenuMusic = self.loadMusic('audio/music/menuSong.mp3')
        self.level1IntroMusic = self.loadMusic('audio/music/level-1-intro.mp3')
        self.level1LoopMusic = self.loadMusic('audio/music/level-1.mp3')
        self.level2IntroMusic = self.loadMusic('audio/music/level-2-intro.mp3')
        self.level2LoopMusic = self.loadMusic('audio/music/level-2.mp3')
        self.gameOverMusic = self.loadMusic('audio/music/game-over.mp3')
        self.levelComplete = self.loadMusic('audio/music/complete.mp3')

    def processInput(self, dt):

        if inputState.isSet('helpMenu'):
            self.helpMenu.show()
        else:
            self.helpMenu.hide()

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
        damaged = self.actorNP.getAnimControl('damage').isPlaying()
        onGround = self.character.isOnGround()

        if movementInput and onGround and not landing:
            self.playSfx(self.walkSound, interrupt=0, volume=self.volume / 4)

        if movementInput and not landing and not running and not jumping and onGround and not damaged:
            self.actorNP.loop('run')
        elif not movementInput and not landing and not idle and not jumping and onGround and not damaged:
            self.actorNP.loop('idle')
        elif not onGround and not landing and not jumping and not damaged:
            self.actorNP.pose('land', 1)

        self.character.setAngularMovement(omega)
        self.character.setLinearMovement(speed, True)

        # Camera

        startpos = self.characterNP.getPos()

        if inputState.isSet('camLeft'):
            base.camera.setX(base.camera, -50 * globalClock.getDt())
        if inputState.isSet('camRight'):
            base.camera.setX(base.camera, +50 * globalClock.getDt())
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
        elif self.damageSound.status() != self.damageSound.PLAYING:
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
        self.processMovingPlatformContacts()

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

        taskMgr.remove('movingPlatforms')
        taskMgr.remove('updateWorld')
        taskMgr.remove('enemyType1Task')

        self.cx.destroy()
        self.cy.destroy()
        self.cz.destroy()
        self.healthBar.destroy()
        self.t.destroy()
        self.p.destroy()

        nodes = self.aspect2d.getChildren()

        for node in nodes:
            node.removeNode()

        nodes = self.aspect2d.getChildren()

        for node in nodes:
            print node

        nodes = self.render.getChildren()

        for node in nodes:
            node.removeNode()

        nodes = self.render.getChildren()

        for node in nodes:
            print node





        # nodes = self.render.getNodes()



        # nodes = self.render.getChildren()
        #
        # print len(nodes)
        #
        # print nodes[0]
        #
        # for node in nodes:
        #
        #     node.removeNode()
        #
        # nodes = self.aspect2d.getChildren()
        #
        # print len(nodes)
        #
        # for node in nodes:
        #
        #     node.removeNode()

        # number = self.render.getNumNodes()

        # print number

        # for node in nodes:

        #    node[].removeNode()

        self.world = None

    def setupLights(self):
        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.6, 0.6, 0.6, 1))
        alightNP = render.attachNewNode(alight)

        # sun right above
        # Vec3(0, -90, 0)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(0, 0, -90))
        dlight.setColor(Vec4(1, 1, 1, 1))
        self.dlightNP = render.attachNewNode(dlight)

        self.render.clearLight()
        self.render.setLight(alightNP)
        self.render.setLight(self.dlightNP)

    def createMovingRectangle(self, size, position, name, hpr=LVecBase3f(0, 0, 0), maxPos=Vec3(0, 0, 0),
                              minPos=Vec3(0, 0, 0), pathVector=Vec3(0, 0, 0), texture = 0):

        platform = self.createFloatingRectangle(size, position, name, hpr, texture)

        movePlatDict = {'platformNP': platform, 'maxXYZ': maxPos, 'minXYZ': minPos, 'pathVector': pathVector}

        self.movingPlatforms.append(movePlatDict)

        return platform

    def keepPlatformsMoving(self, task):

        for movePlatDict in self.movingPlatforms:

            minX = movePlatDict['minXYZ'].getX()
            minY = movePlatDict['minXYZ'].getY()
            minZ = movePlatDict['minXYZ'].getZ()

            maxX = movePlatDict['maxXYZ'].getX()
            maxY = movePlatDict['maxXYZ'].getY()
            maxZ = movePlatDict['maxXYZ'].getZ()

            position = movePlatDict['platformNP'].getPos()

            curX = position.getX()
            curY = position.getY()
            curZ = position.getZ()

            movX = movePlatDict['pathVector'].getX()
            movY = movePlatDict['pathVector'].getY()
            movZ = movePlatDict['pathVector'].getZ()

            if curX + movX > maxX:
                movePlatDict['pathVector'].setX(movX * -1)

            if curY + movY > maxY:
                movePlatDict['pathVector'].setY(movY * -1)

            if curZ + movZ > maxZ:
                movePlatDict['pathVector'].setZ(movZ * -1)

            if curX + movX < minX:
                movePlatDict['pathVector'].setX(movX * -1)

            if curY + movY < minY:
                movePlatDict['pathVector'].setY(movY * -1)

            if curZ + movZ < minZ:
                movePlatDict['pathVector'].setZ(movZ * -1)

            movePlatDict['platformNP'].setPos(position + movePlatDict['pathVector'])

        return task.cont

    def processMovingPlatformContacts(self):

        for movePlatDict in self.movingPlatforms:

            self.processContactWithMovingPlatform(movePlatDict)

    def processContactWithMovingPlatform(self, movePlatDict):

        secondNode = movePlatDict['platformNP'].node()

        contactResult = self.world.contactTestPair(self.character, secondNode)  # returns a BulletContactResult object

        if len(contactResult.getContacts()) > 0 and secondNode.getCollisionResponse():

            self.characterNP.setPos(self.characterNP.getPos() + movePlatDict['pathVector'])

    def createFloatingRectangle(self, size, position, name, hpr=LVecBase3f(0, 0, 0), texture = 0):

        sizeX = size.getX()
        sizeY = size.getY()
        sizeZ = size.getZ()

        dims = [sizeX,sizeY,sizeZ]
        dims.sort(reverse = True)

        shape = BulletBoxShape(size)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        floorNP.node().addShape(shape)
        floorNP.setPos(position)
        floorNP.setHpr(hpr)

        floorNP.setCollideMask(BitMask32.allOn())

        floorNPModel = loader.loadModel('models/EnvBuildingBlocks/brick-cube/brick.egg')

        if texture == 0:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/brick1.png')
        elif texture == 1:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/brick2.png')
        elif texture == 2:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/brick3.png')
        elif texture == 3:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/brick4.png')
        elif texture == 4:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/stone.png')
        elif texture == 5:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/metal.png')
        elif texture == 6:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/dirt-ground.png')
        elif texture == 7:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/ice-crack.png')
        elif texture == 8:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/cobblestones.png')
        elif texture == 9:
            tex = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/cloud.png')

        tex.setMinfilter(SamplerState.FTLinearMipmapLinear)

        floorNPModel.setTexture(tex, 1)

        floorNPModel.setScale(size * 2)
        floorNPModel.setPos(0, 0, -sizeZ)

        ts = TextureStage.getDefault()

        floorNPModel.setTexOffset(ts, -0.5, -0.5)
        floorNPModel.setTexScale(ts, dims[1], dims[0])

        floorNPModel.reparentTo(floorNP)
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

        return button

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
        base = self.createFloatingRectangle(size2, pos, name + ' - Base')

        texture = loader.loadTexture('models/EnvBuildingBlocks/brick-cube/stone.png')

        model = button.getChild(0)
        model.setTexture(texture, 1)

        model = base.getChild(0)
        model.setTexture(texture, 1)

        self.buttonBases.append(base)

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

    def setupLevel(self, level):

        self.MenuFrame.hide()

        self.setup()

        if level == 1:

            self.popUps['levelTip'].start()
            self.buildStage1()
            self.addItemsStage1()
            self.addEnemiesStage1()
            self.makePlayer(Vec3(200, 0, 25))
            self.addBackgroundStage1()

            self.levelIntroMusic = self.level1IntroMusic
            self.levelLoopMusic = self.level1LoopMusic

            self.playMusic(self.levelIntroMusic, volume=self.volume / 4)

        elif level == 2:

            self.popUps['levelTip'].start()
            self.buildStage2()
            self.addItemsStage2()
            self.addEnemiesStage2()
            self.makePlayer(Vec3(179, 20, 4))
            self.addBackgroundStage2()

            self.levelIntroMusic = self.level2IntroMusic
            self.levelLoopMusic = self.level2LoopMusic

            self.playMusic(self.levelIntroMusic, volume=self.volume / 4)

        # Task
        taskMgr.add(self.update, 'updateWorld')

    def setup(self):

        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)
        base.disableMouse()

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

        # used in debug mode
        self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
        self.cx = onscreenText(.90, '')
        self.cy = onscreenText(.85, '')
        self.cz = onscreenText(.80, '')

        self.debugNP.hide()
        self.cx.hide()
        self.cy.hide()
        self.cz.hide()

        # World
        self.setupLights()
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

        # holds ghost objects
        self.consumables = []
        self.removeConsumables = []

        # holds dictionary for button actions
        self.buttonsWithSequences = []
        self.removeButtons = []

        # enemy list
        self.enemiesType1 = []

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        self.setupGui()

    def setupGui(self):

        y = 1
        #x = 1366 / 768.0
        x = self.getAspectRatio()

        self.guiFrame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-x, x, 1, -1), pos=(0, 0, 0))

        ui = OnscreenImage(parent = self.guiFrame, image='images/gui.png', pos=(0, 0, 0), scale=(x, y, 1))
        ui.setTransparency(TransparencyAttrib.MAlpha)
        ui.reparentTo(aspect2d)

        self.healthBar = DirectWaitBar(frameSize=(-x / 3.59, x / 3.59, -y / 32.0, y / 30.0),
                                       text="Roby", value=100, range=100, pos=(-.15, 0, -.926))

        self.t = OnscreenText(text = '', pos=(-0.1, 0.916), scale=.1)
        self.p = OnscreenText(text = '', pos=(.97, -.952), scale=.09)

        gameOverImage = OnscreenImage(parent = self.guiFrame, image='images/game-over.png', pos=(0, 0, 0), scale=(x, y, 1))
        gameOverImage.setTransparency(TransparencyAttrib.MAlpha)
        gameOverImage.reparentTo(aspect2d)
        gameOverImage.setColorScale(LVecBase4f(1, 1, 1, 0))

        fadeInGamOverInterval = gameOverImage.colorScaleInterval(4, LVecBase4f(1, 1, 1, 1))

        levelFinished = OnscreenImage(parent = self.guiFrame, image='images/level-finished.png', pos=(0, 0, 0), scale=(x, y, 1))
        levelFinished.setTransparency(TransparencyAttrib.MAlpha)
        levelFinished.reparentTo(aspect2d)
        levelFinished.setColorScale(LVecBase4f(1, 1, 1, 0))

        fadeInlevelFinishedInterval = levelFinished.colorScaleInterval(4, LVecBase4f(1, 1, 1, 1))

        waypoint = OnscreenImage(parent = self.guiFrame, image='images/waypoint.png', pos=(0, 0, 0), scale=(x, y, 1))
        waypoint.setTransparency(TransparencyAttrib.MAlpha)
        waypoint.reparentTo(aspect2d)
        waypoint.setColorScale(LVecBase4f(1, 1, 1, 0))
        waypointFadeIn = waypoint.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        waypointFadeOut = waypoint.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        waypointSeq = Sequence(waypointFadeIn, waypointFadeOut)

        levelTip = OnscreenImage(parent = self.guiFrame, image='images/level-1-tip.png', pos=(0, 0, 0), scale=(x, y, 1))
        levelTip.setTransparency(TransparencyAttrib.MAlpha)
        levelTip.reparentTo(aspect2d)
        levelTip.setColorScale(LVecBase4f(1, 1, 1, 0))
        levelTipFadeIn = levelTip.colorScaleInterval(2, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        levelTipFadeOut = levelTip.colorScaleInterval(3, Vec4(1, 1, 1, 0))

        levelTipSeq = Sequence(levelTipFadeIn, levelTipFadeOut)

        plus5 = OnscreenImage(parent = self.guiFrame, image='images/plus-5.png', pos=(0, 0, 0), scale=(x, y, 1))
        plus5.setTransparency(TransparencyAttrib.MAlpha)
        plus5.reparentTo(aspect2d)
        plus5.setColorScale(LVecBase4f(1, 1, 1, 0))
        plus5FadeIn = plus5.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        plus5FadeOut = plus5.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        plus5Seq = Sequence(plus5FadeIn, plus5FadeOut)

        plus15 = OnscreenImage(parent = self.guiFrame, image='images/plus-15.png', pos=(0, 0, 0), scale=(x, y, 1))
        plus15.setTransparency(TransparencyAttrib.MAlpha)
        plus15.reparentTo(aspect2d)
        plus15.setColorScale(LVecBase4f(1, 1, 1, 0))
        plus15FadeIn = plus15.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        plus15FadeOut = plus15.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        plus15Seq = Sequence(plus15FadeIn, plus15FadeOut)

        minus5 = OnscreenImage(parent = self.guiFrame, image='images/minus-5.png', pos=(0, 0, 0), scale=(x, y, 1))
        minus5.setTransparency(TransparencyAttrib.MAlpha)
        minus5.reparentTo(aspect2d)
        minus5.setColorScale(LVecBase4f(1, 1, 1, 0))
        minus5FadeIn = minus5.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        minus5FadeOut = minus5.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        minus5Seq = Sequence(minus5FadeIn, minus5FadeOut)

        minus15 = OnscreenImage(parent = self.guiFrame, image='images/minus-15.png', pos=(0, 0, 0), scale=(x, y, 1))
        minus15.setTransparency(TransparencyAttrib.MAlpha)
        minus15.reparentTo(aspect2d)
        minus15.setColorScale(LVecBase4f(1, 1, 1, 0))
        minus15FadeIn = minus15.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        minus15FadeOut = minus15.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        minus15Seq = Sequence(minus15FadeIn, minus15FadeOut)

        jumpBoost = OnscreenImage(parent = self.guiFrame, image='images/jump-boost.png', pos=(0, 0, 0), scale=(x, y, 1))
        jumpBoost.setTransparency(TransparencyAttrib.MAlpha)
        jumpBoost.reparentTo(aspect2d)
        jumpBoost.setColorScale(LVecBase4f(1, 1, 1, 0))
        jumpBoostFadeIn = jumpBoost.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        jumpBoostFadeOut = jumpBoost.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        jumpBoostSeq = Sequence(jumpBoostFadeIn, jumpBoostFadeOut)

        speedBoost = OnscreenImage(parent = self.guiFrame, image='images/speed-boost.png', pos=(0, 0, 0), scale=(x, y, 1))
        speedBoost.setTransparency(TransparencyAttrib.MAlpha)
        speedBoost.reparentTo(aspect2d)
        speedBoost.setColorScale(LVecBase4f(1, 1, 1, 0))
        speedBoostFadeIn = speedBoost.colorScaleInterval(1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        speedBoostFadeOut = speedBoost.colorScaleInterval(1, Vec4(1, 1, 1, 0))

        speedBoostSeq = Sequence(speedBoostFadeIn, speedBoostFadeOut)

        superBoost = OnscreenImage(parent = self.guiFrame,image='images/super-boost.png', pos=(0, 0, 0), scale=(x, y, 1))
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

    def addBackgroundStage1(self):

        self.envBack = loader.loadModel('models/EnvBackgrounds/partlysunny/partlysunny.egg')
        self.envBack.setScale(100)
        self.envBack.reparentTo(render)

        skyPos = self.characterNP.getPos()
        skyPos.setZ(skyPos.getZ() - 1000)
        self.envBack.setPos(skyPos)

    def addBackgroundStage2(self):

        self.envBack = loader.loadModel('models/EnvBackgrounds/bluesky/blue_sky_sphere.egg')
        self.envBack.setScale(10)
        self.envBack.reparentTo(render)

        skyPos = self.characterNP.getPos()
        skyPos.setZ(skyPos.getZ() - 1000)
        self.envBack.setPos(skyPos)

    def makePlayer(self, pos):
        # Character
        h = 6.5
        w = 1.3
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        self.characterNP = self.render.attachNewNode(self.character)

        what = 0

        # self.characterNP.setPos(200, 101, 34)
        # self.characterNP.setPos(200, 0, 34)
        # self.characterNP.setPos(350, 0, 4)
        # self.characterNP.setPos(190, 0, 4)

        self.characterNP.setPos(pos)

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

    def enemyStateChanger(self, task):

        # enemyState = {'anchorNode': anchorNode, 'enemyNP': enemyNP, 'pathSequence': 0,
        # 'pathStart': point1, 'idle': False, 'idleTimer': 0, 'patrolling': False, 'detected': False}
        # isStopped()     isPlaying()          loop()

        for enemyDic in self.enemiesType1:

            currTime = trunc(globalClock.getFrameTime())
            maxFromAnchor = enemyDic['maxFromAnchor']
            detectionRange = enemyDic['detectionRange']
            enemySpeed = enemyDic['enemySpeed']

            distanceFromAnchor = enemyDic['enemyNP'].getDistance(enemyDic['anchorNode'])
            distanceFromPlayer = enemyDic['enemyNP'].getDistance(self.characterNP)

            positionEnemy = enemyDic['enemyNP'].getPos()
            positionPlayer = self.characterNP.getPos()

            patrolling = enemyDic['patrolling']
            chasing = enemyDic['chasing']
            waiting = enemyDic['idle']

            contactsWithPlayer = len(self.world.contactTestPair(self.character, enemyDic['enemyNP'].node()).getContacts())

            vect = positionPlayer - positionEnemy
            vect.normalize()

            movement = vect * enemySpeed
            movement.setZ(0)

            enemyMovement = movement + positionEnemy

            actorNP = enemyDic['actorNP']

            running  = actorNP.getAnimControl('run').isPlaying()
            idle = actorNP.getAnimControl('idle').isPlaying()

            if (patrolling or chasing) and not running:
                actorNP.loop('run')

            elif waiting and not idle:
                actorNP.loop('idle')


            if distanceFromPlayer < detectionRange and patrolling:

                enemyDic['patrolling'] = False
                enemyDic['chasing'] = True
                enemyDic['pathSequence'].finish()
                enemyDic['enemyNP'].setPos(positionEnemy)
                enemyDic['enemyNP'].lookAt(self.characterNP)

            elif chasing and distanceFromAnchor < maxFromAnchor and contactsWithPlayer == 0:

                enemyDic['enemyNP'].setPos(enemyMovement)
                enemyDic['enemyNP'].lookAt(self.characterNP)
                enemyDic['enemyNP'].setP(0)


            elif contactsWithPlayer > 0 and chasing:
                enemyDic['chasing'] = False
                enemyDic['idle'] = True
                enemyDic['idleTimerEnd'] = currTime + 1
                self.actorNP.play('damage')
                self.damageSound.play()

                self.healthBar['value'] -= 5
                self.charState['health'] -= 5

                self.actorNP.setColorScale(1.0, 0.1, 0.1, 1.0)


            elif currTime > enemyDic['idleTimerEnd'] and enemyDic['idle']:
                enemyDic['chasing'] = True
                enemyDic['idle'] = False
                self.actorNP.setColorScale(self.actorNP.getColorScale())


            elif distanceFromAnchor >= maxFromAnchor:

                enemyDic['chasing'] = False
                enemyDic['patrolling'] = True

                enemyDic['enemyNP'].setH(90)
                enemyDic['enemyNP'].setPos(enemyDic['pathStart'])
                enemyDic['pathSequence'].loop()


        return task.cont

    def makeEnemy1(self, name, anchorPos, distFromAnchor, maxFromAnchor, detectionRange, enemySpeed):

        # anchor
        anchorNode = NodePath(PandaNode(name + '- floater'))

        anchorNode.setPos(anchorPos)


        # Character
        h = 6.5
        w = 1.4
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        enemy = BulletCharacterControllerNode(shape, 0.4, name)
        enemyNP = self.render.attachNewNode(enemy)
        enemyNP.setPos(anchorPos)

        enemyNP.setH(90)
        enemyNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(enemy)

        # change model to beefy

        actorNP = Actor('models/characters/beefy/beefy.egg', {
            'idle': 'models/characters/beefy/beefy-idle.egg',
            'run': 'models/characters/beefy/beefy-walk.egg'})

        actorNP.reparentTo(enemyNP)
        actorNP.setScale(0.3048)
        actorNP.setH(180)
        actorNP.setPos(0, 0, .2)

        ancX = anchorPos.getX()
        ancY = anchorPos.getY()
        ancZ = anchorPos.getZ()

        point1 = Vec3(ancX + distFromAnchor, ancY + distFromAnchor, ancZ)
        point2 = Vec3(ancX + distFromAnchor, ancY - distFromAnchor, ancZ)
        point3 = Vec3(ancX - distFromAnchor, ancY - distFromAnchor, ancZ)
        point4 = Vec3(ancX - distFromAnchor, ancY + distFromAnchor, ancZ)

        ancX = anchorPos.getX()
        ancY = anchorPos.getY()
        ancZ = anchorPos.getZ()

        h = enemyNP.getH()

        rot1 = Vec3(h + 90, 0, 0)
        rot2 = Vec3(h + 180, 0, 0)
        rot3 = Vec3(h + 270, 0, 0)
        rot4 = Vec3(h + 360, 0, 0)

        path1 = LerpPosInterval(enemyNP, 8, point4, point1)
        turn1 = LerpHprInterval(enemyNP, 1, rot1)

        path2 = LerpPosInterval(enemyNP, 8, point3, point4)
        turn2 = LerpHprInterval(enemyNP, 1, rot2, rot1)

        path3 = LerpPosInterval(enemyNP, 8, point2, point3)
        turn3 = LerpHprInterval(enemyNP, 1, rot3, rot2)

        path4 = LerpPosInterval(enemyNP, 8, point1, point2)
        turn4 = LerpHprInterval(enemyNP, 1, rot4, rot3)

        seq = Sequence(path1, turn1, path2, turn2, path3, turn3, path4, turn4)
        seq.loop()

        enemyState = {'anchorNode': anchorNode, 'enemyNP': enemyNP, 'actorNP': actorNP,'pathSequence': seq,
                      'maxFromAnchor': maxFromAnchor, 'detectionRange': detectionRange, 'enemySpeed': enemySpeed,
                      'pathStart': point1, 'rot1': rot1, 'idle': False, 'idleTimerEnd': 0, 'patrolling': True,
                      'detected': False, 'chasing': False, 'attacking': False, 'returning': False}

        self.enemiesType1.append(enemyState)

        return enemyNP

game = CharacterController()
game.run()