DO $$
DECLARE 
Yearmonth INTEGER := 202205;
Counter INTEGER;
MaxId INTEGER;
Categoryid INTEGER;
BEGIN
SELECT min(categories.id) INTO Counter
FROM categories;
SELECT max(categories.id) INTO MaxId
FROM categories;

WHILE(Counter IS NOT NULL AND Counter <= MaxId) LOOP
   SELECT categories.id into Categoryid
   FROM categories WHERE categories.id = Counter;
    
   INSERT INTO budgeted (categoryid, yearmonth, assigned) VALUES (Categoryid, Yearmonth, 0);
   Counter  := Counter + 1 ;
   END LOOP;
END $$;