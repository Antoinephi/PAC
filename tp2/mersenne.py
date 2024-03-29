import random

class MersenneTwister:
    """Based on the pseudocode in https://en.wikipedia.org/wiki/Mersenne_Twister.
       Generates uniformly distributed 32-bit integers in the range [0, 232 − 1] with the MT19937 algorithm.

       Written by Yaşar Arabacı <yasar11732 et gmail nokta com>
       Modified by C. Bouillaguet
    """

    bitmask_1 = (2 ** 32) - 1
    bitmask_2 = 2 ** 31
    bitmask_3 = (2 ** 31) - 1


    def __init__(self):
        """Class constructor"""
        self.MT = [ i+1 for i in range(624)]
        self.index = 0

    def rand(self):
        """Returns a 32-bit pseudo-random number. This should be equivalent
        to random.getrandbits(32). However, it does not return the
        same value because the seeding process is different.

        >>> mt = MersenneTwister()
        >>> mt.rand()
        4194449
        """
        # once each cell of the MT array has been used, we refresh the whole array
        if self.index == 624:
            self._generate_numbers()
        x = self.MT[self.index]
        self.index += 1
        # modify the content of the MT cell
        return self._f(x)


    def seed(self, seed):
        """Initialize the generator from a seed.

        This is ***not*** identical to random.seed(), because the
        latter is (a bit too) complicated (and it is written in C, as
        a built-in part of Python). See ``clone_python_state`` below.

        Examples:

        >>> mt = MersenneTwister()
        >>> mt.seed(0)
        >>> mt.rand()
        2479041101

        Compare with :
        >>> random.seed(0)
        >>> random.getrandbits(32)
        3626764237

        """
        self.MT[0] = seed
        for i in range(1,624):
            self.MT[i] = ((1812433253 * self.MT[i-1]) ^ ((self.MT[i-1] >> 30) + i)) & self.bitmask_1
        self.index = 624


    def set_state(self, MT):
        """initialize the internal state of the Mersenne Twister.

        The argument must be a list of 624 integers.
        """
        self.MT = MT
        self.index = 624


    def clone_python_state(self):
        """clone the internal state of the python built-in mersenne twister
           into this one. Once this is done, both PRNGs generate the **same**
           random sequence.

        >>> x = MersenneTwister()
        >>> x.clone_python_state()
        >>> for i in range(1000):
        ...     assert x.rand() == random.getrandbits(32)
        """
        s = random.getstate()
        self.index = s[1][-1]
        self.MT = list(s[1][:-1])


    ###### these functions are for internal use only ####

    def _generate_numbers(self):
        """update the MT array. For internal use only."""
        for i in range(624):
            y = (self.MT[i] & self.bitmask_2) + (self.MT[(i + 1 ) % 624] & self.bitmask_3)
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.MT[i] ^= 2567483615
        self.index = 0

    def _f(self, y):
        """function used to filter cells of the MT array."""
        y ^= y >> 11
        y ^= (y << 7) & 2636928640
        y ^= (y << 15) & 4022730752
        y ^= y >> 18
        return y

def _g(y):
    print("y :\n" + "{0:b}".format(y))
    # print("y >> 11 :\n{0:b}".format(y >> 11))
    # y ^= y >> 11
    # print("y ^= y >> 11 :\n" + "{0:b}".format(y))
    print("y << 7 :\n{0:b}".format(y << 7))
    print("2636928640 :\n{0:b}".format(2636928640))
    print("(y << 7) & 2636928640 :\n{0:b}".format((y << 7) & 2636928640))    
    y ^= (y << 7) & 2636928640
    print("y ^= (y << 7) & 2636928640 :\n" + "{0:b}".format(y))
    # y ^= (y << 15) & 4022730752
    # print("y ^= (y << 15) & 4022730752:\n" + "{0:b}".format(y))
    # y ^= y >> 18
    # print("y ^= y >> 18 :\n"+"{0:b}".format(y))

    return y

def f_(y, decallage, shift, masque=None):
    cpt = 0
    tab = []

    # if masque is not None :
    #     bits_faible = []
    #     for i in range(1, decallage+1):
    #         bits_faible += '1'
    #     bits_faible = bin(bits_faible)


    for i in "{0:b}".format(y):            
        if cpt < decallage :
            tab.append(i)
        else :
            val = int(tab[cpt-decallage]) ^ int(i)
            tab.append(str(val))
        cpt = cpt+1
    res = int("".join(tab), 2)

    if shift == 'l' and len("{0:b}".format(res)) > decallage :
        res = (res >> decallage)

    print("{0:b}".format(res))
    return res

y = _g(5236)
# print("---------------")
# y = f_(y, 11, 'r')
# #15 bits de poids faible
# bits_faible = 0b111111111111111
# print(bits_faible)
# mask = y & bits_faible  
# print(mask)
# # bits_fort = 65498251263
# mask_fort = 4022730752 & 65498251263
# print(mask_fort)
# valeur_3_trente = y & 65498251263

# valeur_2_trentefaible = valeur_3_trente ^ (mask_30 & (valeur_2_quinzefaible<<15))


# valeur_2 = valeur_3 ^ ((valeur_2_trentefaible<<15) & mask)

# y = f_(y, 15, 4022730752)
# print(int("{0:b}".format(y)[7:], 2))

# "{0:b}".format(y)[:7]

# y = f_(y, 18, 'r') 
# y = f_(y, 15, 'l') 
# y = f_(y, 7, 'l') 
# y = int("{0:b}".format(y)[15:], 2)
# print("{0:b}".format(y))
# y = int("{0:b}".format(y)[7:], 2)
# print("{0:b}".format(y))
# y = f_(y, 11, 'r')

# print(y)

# print("{0:b}".format((7 << 2) & 0b1100))

