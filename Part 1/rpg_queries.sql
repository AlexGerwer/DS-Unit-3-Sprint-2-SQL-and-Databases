--Find the total number of characters
SELECT COUNT(*) FROM (SELECT "character_id",* FROM "charactercreator_character" 
ORDER BY "character_id" ASC);

--Find the number of charcters in subclass cleric
SELECT COUNT(*) FROM (SELECT "character_ptr_id",* FROM "charactercreator_cleric" 
ORDER BY "character_ptr_id" ASC);

--Find the number of charcters in subclass fighter
SELECT COUNT(*) FROM (SELECT "character_ptr_id",* FROM "charactercreator_fighter" 
ORDER BY "character_ptr_id" ASC);

--Find the number of charcters in subclass mage
SELECT COUNT(*) FROM (SELECT "character_ptr_id",* FROM "charactercreator_mage" 
ORDER BY "character_ptr_id" ASC);

--Find the number of charcters in subclass necromancer
SELECT COUNT(*) FROM (SELECT "character_ptr_id",* FROM "charactercreator_necromancer" 
ORDER BY "character_ptr_id" ASC);

--Find the number of charcters in subclass thief
SELECT COUNT(*) FROM (SELECT "character_ptr_id",* FROM "charactercreator_thief" 
ORDER BY "character_ptr_id" ASC);

--Find the total number of armory items
SELECT COUNT(*) FROM (SELECT "item_id",* FROM "armory_item" 
ORDER BY "item_id" ASC);

--Find the number of armory items that are weapons
SELECT COUNT(*) FROM (SELECT "item_ptr_id" FROM "armory_item", "armory_weapon"
WHERE "item_id" = "item_ptr_id" ORDER BY "item_ptr_id");

--Find the number of armory items that are weapons (alternative)
SELECT COUNT(*) FROM (SELECT "item_id" FROM "armory_item", "armory_weapon"
WHERE "item_id" = "item_ptr_id" ORDER BY "item_id");

--Find the number of armory items that are not weapons (alternative)
SELECT COUNT(*) FROM (SELECT "item_ptr_id" FROM "armory_weapon", "armory_item"
WHERE "item_id" = "item_ptr_id" ORDER BY "item_ptr_id");

--Find the number of armory items each character has
--First test indirect JOIN using implicit JOIN; associate character names with item names using
--charactercreator_character_inventory as the auxiliary data set
SELECT cc.name, ai.name FROM charactercreator_character AS cc,armory_item AS ai,
charactercreator_character_inventory AS cci
WHERE cc.character_id = cci.character_id
AND ai.item_id = cci.item_id;

SELECT cc.character_id, SUM(ai.item_id) FROM charactercreator_character AS cc,armory_item AS ai,
charactercreator_character_inventory AS cci
WHERE cc.character_id = cci.character_id
AND ai.item_id = cci.item_id
GROUP BY cc.character_id LIMIT 20;

--Fimd how many weapon items each character has
--Test grouping first
SELECT cc.character_id, ai.item_id, aw.item_ptr_id 
FROM charactercreator_character AS cc,armory_item AS ai,armory_weapon AS aw,
charactercreator_character_inventory AS cci
WHERE cc.character_id = cci.character_id 
AND ai.item_id = cci.item_id
AND ai.item_id = aw.item_ptr_id;

SELECT cc.character_id, SUM(aw.item_ptr_id) FROM charactercreator_character AS cc,armory_item AS ai,armory_weapon AS aw,
charactercreator_character_inventory AS cci
WHERE cc.character_id = cci.character_id 
AND ai.item_id = cci.item_id
AND ai.item_id = aw.item_ptr_id
GROUP BY cc.character_id LIMIT 20;

--Find the average number of items that a character has
SELECT cc.character_id, AVG(ai.item_id) FROM charactercreator_character AS cc,armory_item AS ai,
charactercreator_character_inventory AS cci
WHERE cc.character_id = cci.character_id
AND ai.item_id = cci.item_id;

--Find the average number of weapons that a character has
SELECT cc.character_id, AVG(aw.item_ptr_id) FROM charactercreator_character AS cc,armory_item AS ai,armory_weapon AS aw,
charactercreator_character_inventory AS cci
WHERE cc.character_id = cci.character_id 
AND ai.item_id = cci.item_id
AND ai.item_id = aw.item_ptr_id;