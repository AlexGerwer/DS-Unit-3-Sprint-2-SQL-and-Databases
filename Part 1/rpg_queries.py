"""
Assignment - Part 1, Querying a Database
"""
import sqlite3
conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()

# Find the total number of characters\
TNC = curs.execute('SELECT COUNT(*) \
                   FROM (SELECT "character_id",* \
                         FROM "charactercreator_character" \
                         ORDER BY "character_id" ASC);' \
                  ).fetchall()
print ('The total number of characters =', ' '.join(map(str, TNC[0])), '\n')

# Find the number of charcters in subclass cleric
NCC = curs.execute('SELECT COUNT(*) \
                  FROM (SELECT "character_ptr_id",* \
                        FROM "charactercreator_cleric" \
                        ORDER BY "character_ptr_id" ASC);' \
                  ).fetchall()
print ('The number of characters in subclass cleric =',\
       ' '.join(map(str, NCC[0])), '\n')

# Find the number of charcters in subclass fighter
NCF = curs.execute('SELECT COUNT(*) \
                  FROM (SELECT "character_ptr_id",* \
                        FROM "charactercreator_fighter" \
                        ORDER BY "character_ptr_id" ASC);' \
                  ).fetchall()
print ('The number of characters in subclass fighter =',\
       ' '.join(map(str, NCF[0])), '\n')

# Find the number of charcters in subclass mage
NCM = curs.execute('SELECT COUNT(*) \
                   FROM (SELECT "character_ptr_id",* \
                         FROM "charactercreator_mage" \
                         ORDER BY "character_ptr_id" ASC);' \
                  ).fetchall()
print ('The number of characters in subclass mage =',\
       ' '.join(map(str, NCM[0])), '\n')

# Find the number of charcters in subclass necromancer
NCN = curs.execute('SELECT COUNT(*) \
                   FROM (SELECT "character_ptr_id",* \
                         FROM "charactercreator_necromancer" \
                         ORDER BY "character_ptr_id" ASC);' \
                   ).fetchall()
print ('The number of characters in subclass necromancer =',\
       ' '.join(map(str, NCN[0])), '\n')

# Find the number of charcters in subclass thief
NCT = curs.execute('SELECT COUNT(*) \
                   FROM (SELECT "character_ptr_id",* \
                         FROM "charactercreator_thief" \
                         ORDER BY "character_ptr_id" ASC);' \
                   ).fetchall()
print ('The number of characters in subclass thief =',\
       ' '.join(map(str, NCT[0])), '\n')

# Find the total number of armory items
NAT = curs.execute('SELECT COUNT(*) \
                   FROM (SELECT "item_id",* FROM "armory_item" \
                   ORDER BY "item_id" ASC);' \
                   ).fetchall()
print ('The total number of armory items =', ' '.join(map(str, NAT[0])), '\n')

# Find the number of armory items that are weapons
NAW1 = curs.execute('SELECT COUNT(*) \
                   FROM (SELECT "item_ptr_id" \
                         FROM "armory_item", "armory_weapon" \
                         WHERE "item_id" = "item_ptr_id" \
                         ORDER BY "item_ptr_id");' \
                  ).fetchall()
print ('The number of armory items which are weapons =',\
       ' '.join(map(str, NAW1[0])), '\n')

# Find the number of armory items that are weapons (alternative)
NAW2 = curs.execute('SELECT COUNT(*) \
                    FROM (SELECT "item_id" \
                          FROM "armory_item", "armory_weapon" \
                          WHERE "item_id" = "item_ptr_id" \
                          ORDER BY "item_id");' \
                   ).fetchall()
print ('The number of armory items which are weapons (alternate method) =',\
        ' '.join(map(str, NAW2[0])), '\n')

# Find the number of armory items that are not weapons
import numpy as np
NNW = np.subtract(NAT, NAW1)
print ('The number of armory items which are not weapons =', ' '.join(map(str, NNW[0])) , '\n')



# Find the number of armory items each character has
# First test indirect JOIN using implicit JOIN
# associate character names with item names using
# charactercreator_character_inventory as the auxiliary data set
AEC = curs.execute('SELECT cc.name, \
                   SUM(ai.item_id) \
                   FROM charactercreator_character AS cc,armory_item AS ai, \
                        charactercreator_character_inventory AS cci \
                   WHERE cc.character_id = cci.character_id \
                   AND ai.item_id = cci.item_id \
                   GROUP BY cc.character_id LIMIT 20;' \
                   ).fetchall()
print ('The number of armory items each character has:')
l = AEC
width = max(len(e) for t in l for e in t[:-1]) + 1
format=('%%-%ds' % width) * len(l[0])
print ('\n'.join(format % tuple(t) for t in l))
print ('\n')

# Fimd how many weapon items each character has
# Test grouping first
WEC = curs.execute('SELECT cc.name, SUM(aw.item_ptr_id) \
                   FROM charactercreator_character AS cc, \
                        armory_item AS ai,armory_weapon AS aw, \
                        charactercreator_character_inventory AS cci \
                   WHERE cc.character_id = cci.character_id \
                   AND ai.item_id = cci.item_id \
                   AND ai.item_id = aw.item_ptr_id \
                   GROUP BY cc.character_id LIMIT 20;' \
                   ).fetchall()
print ('The number of weapon items each character has:')
l = WEC
width = max(len(e) for t in l for e in t[:-1]) + 1
format=('%%-%ds' % width) * len(l[0])
print ('\n'.join(format % tuple(t) for t in l))
print ('\n')

# Find the average number of items that a character has
AIC = curs.execute('SELECT AVG(ai.item_id) \
                   FROM charactercreator_character AS cc,armory_item AS ai, \
                        charactercreator_character_inventory AS cci \
                   WHERE cc.character_id = cci.character_id \
                   AND ai.item_id = cci.item_id;' \
                   ).fetchall()
print ('The average number of items each character has =',\
       ' '.join(map(str, AIC[0])), '\n')

# Find the average number of weapons that a character has
AWC = curs.execute('SELECT AVG(aw.item_ptr_id) \
                   FROM charactercreator_character AS cc, \
                        armory_item AS ai,armory_weapon AS aw, \
                        charactercreator_character_inventory AS cci \
                   WHERE cc.character_id = cci.character_id \
                   AND ai.item_id = cci.item_id \
                   AND ai.item_id = aw.item_ptr_id;' \
                   ).fetchall()
print ('The average number of weapons each character has =',\
       ' '.join(map(str, AWC[0])), '\n')

curs.close()
conn.commit()
