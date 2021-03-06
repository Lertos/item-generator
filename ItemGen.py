import sys
import json
from functools import partial
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QCompleter, QFormLayout, QPushButton, QCheckBox, QRadioButton
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont

#---------------------
#   Setup
#---------------------

fileName = 'ItemList.json'
itemDictionarySetup = ['id','name','examine','isStackable','shopValue','haValue','laValue','type','meta']
typeSetupIndex = itemDictionarySetup.index('type')

#List that holds all information of each item
itemstest = None
itemList = {}


#List that holds only the item ids
itemIDList = []


#---------------------
#   GUI Class
#---------------------

class ItemGen(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 825)
        self.setWindowTitle("Item Generator")


        #=Item Search
        self.tbItemSearch = self.addTextbox(self, 10, '', 70)
        self.btnItemSearch = self.addButton(self, 10, 'Load Item', 280, 70)
        self.btnClear = self.addButton(self, 10, 'Clear', 360, 70)

        self.btnItemSearch.clicked.connect(self.loadExistingItem)
        self.btnClear.clicked.connect(self.clearAndResetAllFields)
        

        #=ItemID
        self.lblItemID = self.addLabel(self, 50, 'ItemID')
        self.tbItemID = self.addTextbox(self, 50, '')

        #=Display Name
        self.lblDisplay = self.addLabel(self, 75, 'Display')
        self.tbDisplay = self.addTextbox(self, 75, '')

        #=Examine
        self.lblExamine = self.addLabel(self, 100, 'Examine')
        self.tbExamine = self.addTextbox(self, 100, '')

        #=IsStackable
        self.lblIsStackable = self.addLabel(self, 125, 'IsStackable')
        self.tbIsStackable = self.addCheckbox(self, 125)

        #=Shop Value
        self.lblShopValue = self.addLabel(self, 150, 'ShopValue')
        self.tbShopValue = self.addTextbox(self, 150, '0')

        #=HA Value
        self.lblHAValue = self.addLabel(self, 175, 'HAValue')
        self.tbHAValue = self.addTextbox(self, 175, '0')

        #=LA Value
        self.lblLAValue = self.addLabel(self, 200, 'LAValue')
        self.tbLAValue = self.addTextbox(self, 200, '0')

        #=Item Type
        self.rbTypeOther = self.addRadiobutton(self, 225, 'Other', 100)
        self.rbTypeQuest = self.addRadiobutton(self, 250, 'Quest', 100)
        self.rbTypeGear = self.addRadiobutton(self, 225, 'Gear', 210)
        self.rbTypeFood = self.addRadiobutton(self, 250, 'Food', 210)
        self.rbTypePotion = self.addRadiobutton(self, 225, 'Potion', 310)

        self.rbTypeQuest.toggled.connect(self.typeRadioButton)
        self.rbTypeOther.toggled.connect(self.typeRadioButton)
        self.rbTypeGear.toggled.connect(self.typeRadioButton)
        self.rbTypeFood.toggled.connect(self.typeRadioButton)
        self.rbTypePotion.toggled.connect(self.typeRadioButton)


        #------------------------
        #   Food Section
        #------------------------
        self.lblFoodHealthGained = self.addLabel(self, 300, 'HealthGained')
        self.tbFoodHealthGained = self.addTextbox(self, 300, '')

        self.lblFoodOutputItem = self.addLabel(self, 325, 'OutputItem')
        self.tbFoodOutputItem = self.addTextbox(self, 325, '')

        self.lblFoodTimesEaten = self.addLabel(self, 350, 'TimesEaten')
        self.tbFoodTimesEaten = self.addTextbox(self, 350, '1')


        #------------------------
        #   Potion Section
        #------------------------
        self.lblIsBoost = self.addLabel(self, 300, 'IsBoost')
        self.cbIsBoost = self.addCheckbox(self, 300)

        self.lblBoostStats = self.addLabel(self, 325, 'BoostStats')
        self.tbBoostStats = self.addTextbox(self, 325, '')

        self.lblBoostLevels = self.addLabel(self, 350, 'BoostLevels')
        self.tbBoostLevels = self.addTextbox(self, 350, '')

        self.lblAntipoison = self.addLabel(self, 375, 'Antipoison (s)')
        self.tbAntipoison = self.addTextbox(self, 375, '0')

        self.lblSuperAntipoison = self.addLabel(self, 400, 'Antifire (s)')
        self.tbSuperAntipoison = self.addTextbox(self, 400, '0')

        self.lblAntifire = self.addLabel(self, 425, 'Super Antipoison (s)')
        self.tbAntifire = self.addTextbox(self, 425, '0')

        self.lblCuresVenom = self.addLabel(self, 450, 'CuresVenom')
        self.cbCuresVenom = self.addCheckbox(self, 450)

        self.lblIsAntivenom = self.addLabel(self, 475, 'IsAntivenom')
        self.cbIsAntivenom = self.addCheckbox(self, 475)

        self.lblRestorePrayer = self.addLabel(self, 500, 'RestorePrayer')
        self.tbRestorePrayer = self.addTextbox(self, 500, '0')

        self.lblRestoreStats = self.addLabel(self, 525, 'RestoreStats')
        self.tbRestoreStats = self.addTextbox(self, 525, '0')


        #------------------------
        #   Quest Section
        #------------------------
        self.lblQuestID = self.addLabel(self, 300, 'QuestID')
        self.tbQuestID = self.addTextbox(self, 300, '')


        #------------------------
        #   Gear Section
        #------------------------
        self.lblSlot = self.addLabel(self, 300, 'Slot')
        self.tbSlot = self.addTextbox(self, 300, '')

        self.lblIs2Handed = self.addLabel(self, 325, 'Is2Handed')
        self.cbIs2Handed = self.addCheckbox(self, 325)

        self.lblAttStab = self.addLabel(self, 350, 'AttStab')
        self.tbAttStab = self.addTextbox(self, 350, '0')

        self.lblAttSlash = self.addLabel(self, 375, 'AttSlash')
        self.tbAttSlash = self.addTextbox(self, 375, '0')

        self.lblAttCrush = self.addLabel(self, 400, 'AttCrush')
        self.tbAttCrush = self.addTextbox(self, 400, '0')

        self.lblAttRanged = self.addLabel(self, 425, 'AttRanged')
        self.tbAttRanged = self.addTextbox(self, 425, '0')

        self.lblAttMagic = self.addLabel(self, 450, 'AttMagic')
        self.tbAttMagic = self.addTextbox(self, 450, '0')

        self.lblDefStab = self.addLabel(self, 475, 'DefStab')
        self.tbDefStab = self.addTextbox(self, 475, '0')

        self.lblDefSlash = self.addLabel(self, 500, 'DefSlash')
        self.tbDefSlash = self.addTextbox(self, 500, '0')

        self.lblDefCrush = self.addLabel(self, 525, 'DefCrush')
        self.tbDefCrush = self.addTextbox(self, 525, '0')

        self.lblDefRanged = self.addLabel(self, 550, 'DefRanged')
        self.tbDefRanged = self.addTextbox(self, 550, '0')

        self.lblDefMagic = self.addLabel(self, 575, 'DefMagic')
        self.tbDefMagic = self.addTextbox(self, 575, '0')

        self.lblBonusStr = self.addLabel(self, 600, 'BonusStr')
        self.tbBonusStr = self.addTextbox(self, 600, '0')

        self.lblBonusRangedStr = self.addLabel(self, 625, 'BonusRangedStr')
        self.tbBonusRangedStr = self.addTextbox(self, 625, '0')

        self.lblBonusMagicStr = self.addLabel(self, 650, 'BonusMagicStr')
        self.tbBonusMagicStr = self.addTextbox(self, 650, '0')

        self.lblBonusPrayer = self.addLabel(self, 675, 'BonusPrayer')
        self.tbBonusPrayer = self.addTextbox(self, 675, '0')

        self.lblAttackSpeed = self.addLabel(self, 700, 'AttackSpeed')
        self.tbAttackSpeed = self.addTextbox(self, 700, '')

        self.lblQuestNeeded = self.addLabel(self, 725, 'QuestNeeded')
        self.tbQuestNeeded = self.addTextbox(self, 725, '')

        self.lblSkillsNeeded = self.addLabel(self, 750, 'SkillsNeeded')
        self.tbSkillsNeeded = self.addTextbox(self, 750, '')

        self.lblLevelsNeeded = self.addLabel(self, 775, 'LevelsNeeded')
        self.tbLevelsNeeded = self.addTextbox(self, 775, '')


        self.btnCreate = self.addButton(self, 800, 'Create Item', 110, 120)
        self.btnCreate.clicked.connect(partial(self.addNewItem,action='create'))

        self.btnUpdate = self.addButton(self, 800, 'Update Item', 240, 120)
        self.btnUpdate.clicked.connect(partial(self.addNewItem,action='update'))


        self.lblErrorMessage = self.addLabel(self, 725, '')
        self.lblErrorMessage.setStyleSheet("color: red;")
        self.lblErrorMessage.setAlignment(Qt.AlignCenter)
        self.lblErrorMessage.resize(460, 20)


        #=Completer and setup
        self.fillCompleterData()


        #Hide all sub sections to start with
        self.resetAllMainFields()
        self.hideAllSubFields()


    #-- Adds a label with default positioning and behavior
    def addLabel(self, parent, yPos, text):
        label = QLabel(parent)
        label.setText(text)

        label.move(10, yPos)
        label.resize(130, 20)

        label.setAlignment(Qt.AlignRight)
        label.setStyleSheet("padding-top: 4px; padding-right: 4px") 
        
        return label


    #-- Adds a line edit with default positioning and behavior
    def addTextbox(self, parent, yPos, text, xPos=140):
        textbox = QLineEdit(parent)
        textbox.setText(text)

        textbox.move(xPos, yPos)
        textbox.resize(200, 20)
        
        return textbox


    #-- Adds a button with default positioning but not connecting a function to it
    def addButton(self, parent, yPos, text, xPos=350, xSize=120):
        button = QPushButton(parent)
        button.setText(text)

        button.move(xPos, yPos)
        button.resize(xSize, 20)
        
        return button


    #-- Adds a checkbox with default positioning but not connecting a function to it
    def addCheckbox(self, parent, yPos, xPos=140):
        checkbox = QCheckBox(parent)
        checkbox.move(xPos, yPos)

        checkbox.setStyleSheet("padding-top: 4px;") 
        
        return checkbox


    #-- Adds a radio button with default positioning but not connecting a function to it
    def addRadiobutton(self, parent, yPos, text, xPos):
        radioButton = QRadioButton(parent)
        radioButton.setText(text)

        radioButton.move(xPos, yPos)

        radioButton.setStyleSheet("padding-top: 4px;") 
        
        return radioButton


    #-- Handles the switching of type sections
    def typeRadioButton(self):
        self.hideAllSubFields()

        if self.sender().isChecked():
            buttonText = self.sender().text()

            if buttonText == 'Quest':
                self.showQuestSection()
            elif buttonText == 'Food':
                self.showFoodSection()
            elif buttonText == 'Potion':
                self.showPotionSection()
            elif buttonText == 'Gear':
                self.showGearSection()


    #-- Shows Quest section
    def showQuestSection(self):
        self.lblQuestID.show()
        self.tbQuestID.show()


    #-- Shows Gear section
    def showGearSection(self):
        self.lblSlot.show()
        self.tbSlot.show()
        self.lblIs2Handed.show()
        self.cbIs2Handed.show()
        self.lblAttStab.show()
        self.tbAttStab.show()
        self.lblAttSlash.show()
        self.tbAttSlash.show()
        self.lblAttCrush.show()
        self.tbAttCrush.show()
        self.lblAttRanged.show()
        self.tbAttRanged.show()
        self.lblAttMagic.show()
        self.tbAttMagic.show()
        self.lblDefStab.show()
        self.tbDefStab.show()
        self.lblDefSlash.show()
        self.tbDefSlash.show()
        self.lblDefCrush.show()
        self.tbDefCrush.show()
        self.lblDefRanged.show()
        self.tbDefRanged.show()
        self.lblDefMagic.show()
        self.tbDefMagic.show()
        self.lblBonusStr.show()
        self.tbBonusStr.show()
        self.lblBonusRangedStr.show()
        self.tbBonusRangedStr.show()
        self.lblBonusMagicStr.show()
        self.tbBonusMagicStr.show()
        self.lblBonusPrayer.show()
        self.tbBonusPrayer.show()
        self.lblAttackSpeed.show()
        self.tbAttackSpeed.show()
        self.lblQuestNeeded.show()
        self.tbQuestNeeded.show()
        self.lblSkillsNeeded.show()
        self.tbSkillsNeeded.show()
        self.lblLevelsNeeded.show()
        self.tbLevelsNeeded.show()


    #-- Shows Food section
    def showFoodSection(self):
        self.lblFoodHealthGained.show()
        self.tbFoodHealthGained.show()
        self.lblFoodOutputItem.show()
        self.tbFoodOutputItem.show()
        self.lblFoodTimesEaten.show()
        self.tbFoodTimesEaten.show()


    #-- Shows Potion section
    def showPotionSection(self):
        self.lblIsBoost.show()
        self.cbIsBoost.show()
        self.lblBoostStats.show()
        self.tbBoostStats.show()
        self.lblBoostLevels.show()
        self.tbBoostLevels.show()
        self.lblAntipoison.show()
        self.tbAntipoison.show()
        self.lblSuperAntipoison.show()
        self.tbSuperAntipoison.show()
        self.lblAntifire.show()
        self.tbAntifire.show()
        self.lblCuresVenom.show()
        self.cbCuresVenom.show()
        self.lblIsAntivenom.show()
        self.cbIsAntivenom.show()
        self.lblRestorePrayer.show()
        self.tbRestorePrayer.show()
        self.lblRestoreStats.show()
        self.tbRestoreStats.show()


    #-- Clears and resets all fields
    def clearAndResetAllFields(self):
        self.resetAllMainFields()
        self.hideAllSubFields()


    #-- Resets all main fields
    def resetAllMainFields(self):
        self.tbItemSearch.setText('')
        self.tbItemID.setText('')
        self.tbDisplay.setText('')
        self.tbExamine.setText('')
        self.tbIsStackable.setChecked(False)
        self.tbShopValue.setText('0')
        self.tbHAValue.setText('0')
        self.tbLAValue.setText('0')
        self.rbTypeOther.setChecked(True)
        self.rbTypeQuest.setChecked(False)
        self.rbTypeGear.setChecked(False)
        self.rbTypeFood.setChecked(False)
        self.rbTypePotion.setChecked(False)
        self.lblErrorMessage.setText('')


    #-- Hides all sub category fields
    def hideAllSubFields(self):
        self.lblFoodHealthGained.hide()
        self.tbFoodHealthGained.hide()
        self.tbFoodHealthGained.setText('')
        self.lblFoodOutputItem.hide()
        self.tbFoodOutputItem.hide()
        self.tbFoodOutputItem.setText('')
        self.lblFoodTimesEaten.hide()
        self.tbFoodTimesEaten.hide()
        self.tbFoodTimesEaten.setText('1')

        self.lblIsBoost.hide()
        self.cbIsBoost.hide()
        self.cbIsBoost.setChecked(False)
        self.lblBoostStats.hide()
        self.tbBoostStats.hide()
        self.tbBoostStats.setText('')
        self.lblBoostLevels.hide()
        self.tbBoostLevels.hide()
        self.tbBoostLevels.setText('')
        self.lblAntipoison.hide()
        self.tbAntipoison.hide()
        self.tbAntipoison.setText('0')
        self.lblSuperAntipoison.hide()
        self.tbSuperAntipoison.hide()
        self.tbSuperAntipoison.setText('0')
        self.lblAntifire.hide()
        self.tbAntifire.hide()
        self.tbAntifire.setText('0')
        self.lblCuresVenom.hide()
        self.cbCuresVenom.hide()
        self.cbCuresVenom.setChecked(False)
        self.lblIsAntivenom.hide()
        self.cbIsAntivenom.hide()
        self.cbIsAntivenom.setChecked(False)
        self.lblRestorePrayer.hide()
        self.tbRestorePrayer.hide()
        self.tbRestorePrayer.setText('0')
        self.lblRestoreStats.hide()
        self.tbRestoreStats.hide()
        self.tbRestoreStats.setText('0')

        self.lblQuestID.hide()
        self.tbQuestID.hide()
        self.tbQuestID.setText('')

        self.lblSlot.hide()
        self.tbSlot.hide()
        self.tbSlot.setText('')
        self.lblIs2Handed.hide()
        self.cbIs2Handed.hide()
        self.cbIs2Handed.setChecked(False)
        self.lblAttStab.hide()
        self.tbAttStab.hide()
        self.tbAttStab.setText('0')
        self.lblAttSlash.hide()
        self.tbAttSlash.hide()
        self.tbAttSlash.setText('0')
        self.lblAttCrush.hide()
        self.tbAttCrush.hide()
        self.tbAttCrush.setText('0')
        self.lblAttRanged.hide()
        self.tbAttRanged.hide()
        self.tbAttRanged.setText('0')
        self.lblAttMagic.hide()
        self.tbAttMagic.hide()
        self.tbAttMagic.setText('0')
        self.lblDefStab.hide()
        self.tbDefStab.hide()
        self.tbDefStab.setText('0')
        self.lblDefSlash.hide()
        self.tbDefSlash.hide()
        self.tbDefSlash.setText('0')
        self.lblDefCrush.hide()
        self.tbDefCrush.hide()
        self.tbDefCrush.setText('0')
        self.lblDefRanged.hide()
        self.tbDefRanged.hide()
        self.tbDefRanged.setText('0')
        self.lblDefMagic.hide()
        self.tbDefMagic.hide()
        self.tbDefMagic.setText('0')
        self.lblBonusStr.hide()
        self.tbBonusStr.hide()
        self.tbBonusStr.setText('0')
        self.lblBonusRangedStr.hide()
        self.tbBonusRangedStr.hide()
        self.tbBonusRangedStr.setText('0')
        self.lblBonusMagicStr.hide()
        self.tbBonusMagicStr.hide()
        self.tbBonusMagicStr.setText('0')
        self.lblBonusPrayer.hide()
        self.tbBonusPrayer.hide()
        self.tbBonusPrayer.setText('0')
        self.lblAttackSpeed.hide()
        self.tbAttackSpeed.hide()
        self.tbAttackSpeed.setText('')
        self.lblQuestNeeded.hide()
        self.tbQuestNeeded.hide()
        self.tbQuestNeeded.setText('')
        self.lblSkillsNeeded.hide()
        self.tbSkillsNeeded.hide()
        self.tbSkillsNeeded.setText('')
        self.lblLevelsNeeded.hide()
        self.tbLevelsNeeded.hide()
        self.tbLevelsNeeded.setText('')


    #-- Adds a new item to the item list, converting fields into the mapping of dictionary keys
    def addNewItem(self, action):
        itemID = self.tbItemID.text()
        
        #If action='create' - check to make sure the itemID DOES NOT exist, adding it to the lookup itemID list
        if action == 'create':
            if itemID in itemIDList:
                self.lblErrorMessage.setText('That ItemID already exists')
                return

            #Add the new ItemID to the ItemIDList so that duplicates won't happen
            itemIDList.append(itemID)
            self.fillCompleterData()

            itemList[itemID] = {}
        #If action='update' - check to make sure the itemID DOES exist
        elif action == 'update':
            if itemID not in itemIDList:
                self.lblErrorMessage.setText('The ItemID provided doesnt exist so it cannot be updated')
                return


        itemList[itemID]['name'] = self.tbDisplay.text()
        itemList[itemID]['examine'] = self.tbExamine.text()
        itemList[itemID]['isStackable'] = self.tbIsStackable.isChecked()
        itemList[itemID]['shopValue'] = self.tbShopValue.text()
        itemList[itemID]['haValue'] = self.tbHAValue.text()
        itemList[itemID]['laValue'] = self.tbLAValue.text()

        itemType = ''

        if self.rbTypeQuest.isChecked():
            itemType = 'quest'
        elif self.rbTypeOther.isChecked():
            itemType = 'other'
        elif self.rbTypeGear.isChecked():
            itemType = 'gear'
        elif self.rbTypeFood.isChecked():
            itemType = 'food'
        elif self.rbTypePotion.isChecked():
            itemType = 'potion'

        if itemType == '':
            self.lblErrorMessage.setText('No ItemType was specified')
            return

        itemList[itemID]['type'] = itemType
        itemList[itemID]['meta'] = self.addItemMeta(itemList[itemID], itemType)

        #Reset all fields
        self.resetAllMainFields()
        self.hideAllSubFields()

        #Add the new item to the file and save it
        saveItemList()


    #-- Adds the item meta of an item as a sub dictionary
    def addItemMeta(self, dictKey, itemType):
        tempDict = {}

        if itemType == 'gear':
            tempDict['slot'] = self.tbSlot.text()
            tempDict['is2Handed'] = self.cbIs2Handed.isChecked()
            tempDict['attStab'] = self.tbAttStab.text()
            tempDict['attSlash'] = self.tbAttSlash.text()
            tempDict['attCrush'] = self.tbAttCrush.text()
            tempDict['attRanged'] = self.tbAttRanged.text()
            tempDict['attMagic'] = self.tbAttMagic.text()
            tempDict['defStab'] = self.tbDefStab.text()
            tempDict['defSlash'] = self.tbDefSlash.text()
            tempDict['defCrush'] = self.tbDefCrush.text()
            tempDict['defRanged'] = self.tbDefRanged.text()
            tempDict['defMagic'] = self.tbDefMagic.text()
            tempDict['bonusStr'] = self.tbBonusStr.text()
            tempDict['bonusRangedStr'] = self.tbBonusRangedStr.text()
            tempDict['bonusMagicStr'] = self.tbBonusMagicStr.text()
            tempDict['bonusPrayer'] = self.tbBonusPrayer.text()
            tempDict['attackSpeed'] = self.tbAttackSpeed.text()
            tempDict['questNeeded'] = self.tbQuestNeeded.text()
            tempDict['skillsNeeded'] = self.tbSkillsNeeded.text()
            tempDict['levelsNeeded'] = self.tbLevelsNeeded.text()

        elif itemType == 'food':
            tempDict['healthGained'] = self.tbFoodHealthGained.text()
            tempDict['outputItemID'] = self.tbFoodOutputItem.text()
            tempDict['timesEaten'] = self.tbFoodTimesEaten.text()

        elif itemType == 'potion':
            tempDict['isBoost'] = self.cbIsBoost.isChecked()
            tempDict['boostStats'] = self.tbBoostStats.text()
            tempDict['boostLevels'] = self.tbBoostLevels.text()
            tempDict['antipoison'] = self.tbAntipoison.text()
            tempDict['superAntipoison'] = self.tbSuperAntipoison.text()
            tempDict['antifire'] = self.tbAntifire.text()
            tempDict['curesVenom'] = self.cbCuresVenom.isChecked()
            tempDict['isAntivenom'] = self.cbIsAntivenom.isChecked()
            tempDict['restorePrayer'] = self.tbRestorePrayer.text()
            tempDict['restoreStats'] = self.tbRestoreStats.text()

        elif itemType == 'quest':
            tempDict['questID'] = self.tbQuestID.text()

        return tempDict


    #-- Checks the item list for a specific itemID. If found, load the data, mapping dictionary keys to specific fields
    def loadExistingItem(self):
        itemID = self.tbItemSearch.text()
        
        if itemID not in itemIDList:
            self.lblErrorMessage.setText('No Item with that ItemID exists')
            return

        print(itemID)
        print(itemList)
        item = itemList[itemID]

        self.tbItemID.setText(itemID)
        self.tbDisplay.setText(item['name'])
        self.tbExamine.setText(item['examine'])
        self.tbIsStackable.setChecked(item['isStackable'])
        self.tbShopValue.setText(item['shopValue'])
        self.tbHAValue.setText(item['haValue'])
        self.tbLAValue.setText(item['laValue'])

        itemType = item['type']

        if itemType == 'gear':
            self.rbTypeGear.setChecked(True)  
        elif itemType == 'food':
            self.rbTypeFood.setChecked(True)
        elif itemType == 'potion':
            self.rbTypePotion.setChecked(True)
        elif itemType == 'quest':
            self.rbTypeQuest.setChecked(True)
        else:
            self.rbTypeOther.setChecked(True)

        self.loadItemMeta(item['meta'], itemType)


    #-- From the dictionary, load the item meta based on the item type
    def loadItemMeta(self, itemMeta, itemType):
        if itemType == 'gear':
            self.tbSlot.setText(itemMeta['slot'])
            self.cbIs2Handed.setChecked(itemMeta['is2Handed'])
            self.tbAttStab.setText(itemMeta['attStab'])
            self.tbAttSlash.setText(itemMeta['attSlash'])
            self.tbAttCrush.setText(itemMeta['attCrush'])
            self.tbAttRanged.setText(itemMeta['attRanged'])
            self.tbAttMagic.setText(itemMeta['attMagic'])
            self.tbDefStab.setText(itemMeta['defStab'])
            self.tbDefSlash.setText(itemMeta['defSlash'])
            self.tbDefCrush.setText(itemMeta['defCrush'])
            self.tbDefRanged.setText(itemMeta['defRanged'])
            self.tbDefMagic.setText(itemMeta['defMagic'])
            self.tbBonusStr.setText(itemMeta['bonusStr'])
            self.tbBonusRangedStr.setText(itemMeta['bonusRangedStr'])
            self.tbBonusMagicStr.setText(itemMeta['bonusMagicStr'])
            self.tbBonusPrayer.setText(itemMeta['bonusPrayer'])
            self.tbAttackSpeed.setText(itemMeta['attackSpeed'])
            self.tbQuestNeeded.setText(itemMeta['questNeeded'])
            self.tbSkillsNeeded.setText(itemMeta['skillsNeeded'])
            self.tbLevelsNeeded.setText(itemMeta['levelsNeeded'])

        elif itemType == 'food':
            self.tbFoodHealthGained.setText(itemMeta['healthGained'])
            self.tbFoodOutputItem.setText(itemMeta['outputItemID'])
            self.tbFoodTimesEaten.setText(itemMeta['timesEaten'])

        elif itemType == 'potion':
            self.cbIsBoost.setChecked(itemMeta['isBoost'])
            self.tbBoostStats.setText(itemMeta['boostStats'])
            self.tbBoostLevels.setText(itemMeta['boostLevels'])
            self.tbAntipoison.setText(itemMeta['antipoison'])
            self.tbSuperAntipoison.setText(itemMeta['superAntipoison'])
            self.tbAntifire.setText(itemMeta['antifire'])
            self.cbCuresVenom.setChecked(itemMeta['curesVenom'])
            self.cbIsAntivenom.setChecked(itemMeta['isAntivenom'])
            self.tbRestorePrayer.setText(itemMeta['restorePrayer'])
            self.tbRestoreStats.setText(itemMeta['restoreStats'])

        elif itemType == 'quest':
            self.tbQuestID.setText(itemMeta['questID'])


    #-- Used to update the QCompleter with the newest version of the list
    def fillCompleterData(self):
        self.completer = QCompleter(itemIDList, self)
        self.tbItemSearch.setCompleter(self.completer)
        self.tbItemID.setCompleter(self.completer)
        self.tbFoodOutputItem.setCompleter(self.completer)


#---------------------
#   Other Methods
#---------------------

#-- Saves the item dictionary to the output file to update the file with any changes
def saveItemList():

    with open(fileName, mode="w") as itemFile:
        json.dump(itemList, itemFile)   


#---------------------
#   Main Application
#---------------------

#Load Items from the json file
with open(fileName) as itemFile:
    itemList = json.load(itemFile)

#load each item into the list that the completer uses to check for existing items
for key in itemList.keys():
        itemIDList.append(key)


#Start the GUI
app = QApplication(sys.argv)
outputter = ItemGen()
outputter.show()
sys.exit(app.exec_())