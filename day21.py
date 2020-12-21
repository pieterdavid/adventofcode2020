# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Advent of code 2020: day 21
#
# Problem [here](https://adventofcode.com/2020/day/21)

# ## Part 1

# +
ex_in = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

def readFoodList(lines):
    ingredAllergens = []
    for ln in lines:
        pIngred, pAllerg = ln.split(" (contains ")
        ingred = list(pIngred.split())
        allerg = list(pAllerg.rstrip(")").split(", "))
        ingredAllergens.append((ingred, allerg))
    return ingredAllergens

ex_food = readFoodList(ex_in.split("\n"))
print(ex_food)

# +
from collections import defaultdict

def findAllergens(foodList):
    options_perAllerg = {}
    allIngredients = defaultdict(int)
    for f_ingred, f_allerg in foodList:
        for allerg in f_allerg:
            if allerg in options_perAllerg: # already have options: interesect
                presentOpts = options_perAllerg[allerg]
                options_perAllerg[allerg] = [ ingred for ingred in f_ingred if ingred in presentOpts ]
            else: # otherwise, all these are possible
                options_perAllerg[allerg] = f_ingred
        for ingred in f_ingred:
            allIngredients[ingred] += 1

    nAllergens = len(options_perAllerg)
    allergens = dict()
    while nAllergens != len(allergens):
        aFound, iFound = [], []
        ## find those with 1
        for allerg, options in options_perAllerg.items():
            if len(options) == 1:
                allergens[allerg] = options[0]
                aFound.append(allerg)
                iFound.append(options[0])
        ## update options: if found -> empty,
        for fnd in aFound:
            del options_perAllerg[fnd]
        for allerg in options_perAllerg.keys():
            options_perAllerg[allerg] = [ ingred for ingred in options_perAllerg[allerg] if ingred not in iFound ]
        if not aFound:
            raise RuntimeError("None assigned this round, exiting loop")
    return allergens, allIngredients

ex_allergens, ex_allIngredients = findAllergens(ex_food)
ex_allergIngred = set(ex_allergens.values())
ex_sum = 0
for ingred,cnt in ex_allIngredients.items():
    if ingred not in ex_allergIngred:
        print(f"Ingredient {ingred} occurs {cnt:d} times")
        ex_sum += cnt
print(f"Sum: {ex_sum:d}")

# +
with open("inputs/day21.txt") as inF:
    p_food = readFoodList((ln.strip() for ln in inF))

p_allergens, p_allIngredients = findAllergens(p_food)
p_allergIngred = set(p_allergens.values())
p_sum = 0
for ingred,cnt in p_allIngredients.items():
    if ingred not in p_allergIngred:
        p_sum += cnt
print(f"Sum: {p_sum:d}")
# -

# ## Part 2

print(",".join(ingred for allerg,ingred in sorted(ex_allergens.items(), key=lambda elm : elm[0])))
print(",".join(ingred for allerg,ingred in sorted(p_allergens.items(), key=lambda elm : elm[0])))
