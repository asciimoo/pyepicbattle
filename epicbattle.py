#!/usr/bin/env python2.6

from random import choice, random
from configobj import ConfigObj

def randrange(min, max):
    return random() * (max-min) + min

class Creature(object):
    def __init__(self, name=''):
        self.name        = name
        self.strength    = 10
        self.dexterity   = 10
        self.vitality    = 10
        self.wisdom      = 10
        self.intellect   = 10
        self.luck        = 0
        # end of stats, level1 sum: 60
        self.pwn_zone    = 0
        self.charm       = 0
        self.epicness    = 0  # self epicness =P
        self.xp          = 0
        self.level       = 0
        self.items       = {}
        self.stash       = {}
        self.phobias     = {}
        self.pos         = {'x':0, 'y':0, 'z':0}
        self.monkey      = 0  # will be a hash
        self.description = ''

    def _getLife(self):
        self.life = self.vitality * 10
        return self

    def getDamage(self):
        return self.strength * randrange(0.9, 1.1)

    def setDamage(self, dmg):
        self.life -= dmg / (self.dexterity/10.0)

    def getHero(self, f):
        c = ConfigObj(f,raise_errors=True)
        for k,v in c['hero'].items():
            self.__getattribute__(k)
            if k in ['name', 'description']:
                self.__setattr__(k, v)
            else:
                self.__setattr__(k, c['hero'].as_int(k))
        self.items   = c['items']
        self.stash   = c['stash']
        self.phobias = c['phobias']
        return self

    def saveHero(self, f):
        c = ConfigObj()
        c.filename = f
        c['hero'] = {'name': self.name,
                  'strength': self.strength,
                  'dexterity': self.dexterity,
                  'vitality': self.vitality,
                  'wisdom': self.wisdom,
                  'intellect': self.intellect,
                  'luck': self.luck,
                  'charm': self.charm,
                  'epicness': self.epicness,
                  'xp': self.xp,
                  'level': self.level,
                  'monkey': self.monkey,
                  'description': self.description}
        c['items'] = self.items
        c['stash'] = self.stash
        c['phobias'] = self.phobias
        c.write()

# TODOS ;)
# Phobie generator !!
# random name generator
# PHOBIES:
#   The fear of two swords (bisword phobie)
#   The fear of butterflies (bisword phobie)
# body parts

class Item():
    def __init__(self):
        self.owner_mods   = []
        self.target_mods  = []
        self.funs         = {}
        self.price        = 0
        self.requirements = {}
        self.types        = []

class World():
    def __init__(self, creatures):
        self.creatures = creatures

    def happening(self):
        if randrange(0, 1) > 0.9:
            c = choice(self.creatures)
            c.luck += 1
            print '[!] %s gets some luck' % c.name
        if randrange(0, 1) > 0.95:
            c = choice(self.creatures)
            c.epicness += 0.1
            print '[!] %s gets some EPICNEEEEESSS!!!!' % c.name


class EpicBattle():
    def __init__(self, *creatures):
        self.creatures = [c._getLife() for c in creatures]
        self.world = World(creatures) # TODO

    def start(self):
        # TODO positioning
        return self.fight()

    def _lifeCheck(self):
        # TODO filter()
        ret = []
        for k, c in enumerate(self.creatures):
            if c.life <= 0:
                ret.append(k)
        return ret

    def fight(self):
        print '[>] '+ ', '.join(['%s:%f' % (c.name, c.life) for c in self.creatures])
        for i in sorted(self._lifeCheck(), reverse=True):
            print "[!] %s is dead!!" % self.creatures.pop(i).name
        if len(self.creatures) == 1:
            print '[!] MONSTER EPIC WIN!!1!11!'
            return '[!!] %s wins!!' % self.creatures[0].name
        elif len(self.creatures) == 0:
            return '[!] EPIC DIE!!'
        self.world.happening()
        for a in self.creatures:
            for b in self.creatures:
                if a is not b:
                    a.setDamage(b.getDamage())
                    b.setDamage(a.getDamage())

        self.world.happening()
        return self.fight()

if __name__ == '__main__':
    Pot      = Creature('Potato')
    Pot.strength  += 2
    Pot.dexterity -= 2
    asciimoo = Creature().getHero('asciimoo.epic')
    print asciimoo.__dict__
    battle = EpicBattle(Pot, asciimoo, Creature('asdf'))
    print battle.start()
    print asciimoo.__dict__
    asciimoo.saveHero('asciimoo2.epic')



