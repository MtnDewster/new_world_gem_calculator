from PyQt6.QtWidgets import QApplication, QMainWindow, QSpinBox
from PyQt6 import uic
import math, sys, os

dir_path = os.path.dirname(os.path.realpath(__file__))

mote_dict = {
    'Air': ['Jasper', 'Topaz'],
    'Death': ['Moonstone', 'Sapphire'],
    'Earth': ['Amber', 'Emerald'],
    'Fire': ['Carnelian', 'Ruby'],
    'Life': ['Diamond', 'Onyx'],
    'Soul': ['Amethyst', 'Malachite', 'Opal'],
    'Water': ['Aquamarine']
}

empty_motes_needed_dict = {
    'Air': 0,
    'Death': 0,
    'Earth': 0,
    'Fire': 0,
    'Life': 0,
    'Soul': 0,
    'Water': 0
}

mote_surname = {
    3: ' Wisp',
    4: ' Essence',
    5: ' Quintessence'
}

gem_prefix = {
    3: '',
    4: 'Brilliant ',
    5: 'Prestine '
}

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(fr'{dir_path}\gem_calculator.ui', self)
        self.setWindowTitle('New World Gem Fusing Calculator')
        self.calculate_button.clicked.connect(self.Calculate)
        self.recipe_selector.currentIndexChanged.connect(self.UpdateRecipe)
        self.reset_values.triggered.connect(self.Reset)
        self.mote_labels = {
            'Air': self.air_mote,
            'Death': self.death_mote,
            'Earth': self.earth_mote,
            'Fire': self.fire_mote,
            'Life': self.life_mote,
            'Soul': self.soul_mote,
            'Water': self.water_mote
        }
        self.gem_labels = {
            'Amber': self.amber_gem,
            'Amethyst': self.amethyst_gem,
            'Aquamarine': self.aquamarine_gem,
            'Carnelian': self.carnelian_gem,
            'Diamond': self.diamond_gem,
            'Emerald': self.emerald_gem,
            'Jasper': self.jasper_gem,
            'Malachite': self.malachite_gem,
            'Moonstone': self.moonstone_gem,
            'Onyx': self.onyx_gem,
            'Opal': self.opal_gem,
            'Ruby': self.ruby_gem,
            'Sapphire': self.sapphire_gem,
            'Topaz': self.topaz_gem
        }
        for k, v in self.mote_labels.items():
            v.setText(f'{k} Wisp:')
        for k, v in self.gem_labels.items():
            v.setText(f'Flawed {k}:')
        self.needed_gems = 3

    def Reset(self):
        spin_boxes = self.findChildren(QSpinBox)
        for spin_box in spin_boxes:
            spin_box.setValue(0)

    def UpdateRecipe(self, new_value):
        match new_value:
            case 0:
                for k, v in self.mote_labels.items():
                    v.setText(f'{k} Wisp:')
                for k, v in self.gem_labels.items():
                    v.setText(f'Flawed {k}:')
                self.needed_gems = 3
            case 1:
                for k, v in self.mote_labels.items():
                    v.setText(f'{k} Essence:')
                for k, v in self.gem_labels.items():
                    v.setText(f'{k}:')
                self.needed_gems = 4
            case 2:
                for k, v in self.mote_labels.items():
                    v.setText(f'{k} Quintessence:')
                for k, v in self.gem_labels.items():
                    v.setText(f'Brilliant {k}:')
                self.needed_gems = 5

    def Calculate(self):
        self.have_everything = True
        self.needed_list.clear()
        self.can_create_list.clear()
        self.needed_motes = empty_motes_needed_dict.copy()
        self.current_gems = {
            'Amber': self.amber_amount.value(),
            'Amethyst': self.amethyst_amount.value(),
            'Aquamarine': self.aquamarine_amount.value(),
            'Carnelian': self.carnelian_amount.value(),
            'Diamond': self.diamond_amount.value(),
            'Emerald': self.emerald_amount.value(),
            'Jasper': self.jasper_amount.value(),
            'Malachite': self.malachite_amount.value(),
            'Moonstone': self.moonstone_amount.value(),
            'Onyx': self.onyx_amount.value(),
            'Opal': self.opal_amount.value(),
            'Ruby': self.ruby_amount.value(),
            'Sapphire': self.sapphire_amount.value(),
            'Topaz': self.topaz_amount.value(),
        }
        self.current_motes = {
            'Air': self.air_amount.value(),
            'Death': self.death_amount.value(),
            'Earth': self.earth_amount.value(),
            'Fire': self.fire_amount.value(),
            'Life': self.life_amount.value(),
            'Soul': self.soul_amount.value(),
            'Water': self.water_amount.value()
        }
        self.can_create = {}
        for k,v in mote_dict.items():
            self.tmp_needed_motes = 0
            for value in v:
                self.num_craft = math.floor(self.current_gems[value] / self.needed_gems)
                if self.num_craft > 0:
                    self.can_create[value] = self.num_craft
                self.tmp_needed_motes += self.num_craft
            self.tmp_motes = self.tmp_needed_motes - self.current_motes[k]
            if self.tmp_motes <= 0:
                self.needed_motes[k] = 0
            else:
                self.needed_motes[k] = self.tmp_motes
                self.have_everything = False
        if self.have_everything == False:
            self.needed_list.addItem('You need to buy/acquire:')
            for k, v in self.needed_motes.items():
                if v != 0:
                    self.needed_list.addItem(f'{k}{mote_surname[self.needed_gems]} - {v}')
        if self.have_everything == True:
            self.needed_list.addItem('You have everything you need to craft!')
        if len(self.can_create) == 0:
            self.can_create_list.addItem('You can\'t fuse any gems :(')
        if len(self.can_create) >= 1:
            self.can_create_list.addItem('Once you have all motes you can craft (w/o bonuses):')
            for k, v in self.can_create.items():
                self.can_create_list.addItem(f'{v} - {gem_prefix[self.needed_gems]}{k}(s).')

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())