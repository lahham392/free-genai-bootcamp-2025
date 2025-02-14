-- Seed Groups
INSERT INTO groups (name) VALUES 
('Greetings'),
('Numbers'),
('Colors'),
('Family'),
('Food');

-- Seed Words
INSERT INTO words (spanish, transliteration, arabic) VALUES 
-- Greetings
('hola', 'هولا', 'مرحبا'),
('buenos días', 'بوينوس دياس', 'صباح الخير'),
('gracias', 'غراثياس', 'شكرا'),

-- Numbers
('uno', 'اونو', 'واحد'),
('dos', 'دوس', 'اثنان'),
('tres', 'تريس', 'ثلاثة'),

-- Colors
('rojo', 'روخو', 'أحمر'),
('azul', 'اثول', 'أزرق'),
('verde', 'بيردي', 'أخضر'),

-- Family
('padre', 'بادري', 'أب'),
('madre', 'مادري', 'أم'),
('hermano', 'إيرمانو', 'أخ'),

-- Food
('pan', 'بان', 'خبز'),
('agua', 'اغوا', 'ماء'),
('leche', 'ليتشي', 'حليب');

-- Link words to groups
-- Greetings
INSERT INTO word_groups (word_id, group_id) 
SELECT w.id, g.id 
FROM words w, groups g 
WHERE w.spanish IN ('hola', 'buenos días', 'gracias') 
AND g.name = 'Greetings';

-- Numbers
INSERT INTO word_groups (word_id, group_id) 
SELECT w.id, g.id 
FROM words w, groups g 
WHERE w.spanish IN ('uno', 'dos', 'tres') 
AND g.name = 'Numbers';

-- Colors
INSERT INTO word_groups (word_id, group_id) 
SELECT w.id, g.id 
FROM words w, groups g 
WHERE w.spanish IN ('rojo', 'azul', 'verde') 
AND g.name = 'Colors';

-- Family
INSERT INTO word_groups (word_id, group_id) 
SELECT w.id, g.id 
FROM words w, groups g 
WHERE w.spanish IN ('padre', 'madre', 'hermano') 
AND g.name = 'Family';

-- Food
INSERT INTO word_groups (word_id, group_id) 
SELECT w.id, g.id 
FROM words w, groups g 
WHERE w.spanish IN ('pan', 'agua', 'leche') 
AND g.name = 'Food';

-- Add some study sessions and reviews
INSERT INTO study_sessions (group_id, study_activity, created_at) 
SELECT id, 'flashcards', datetime('now', '-1 day')
FROM groups 
WHERE name = 'Greetings';

INSERT INTO study_sessions (group_id, study_activity, created_at) 
SELECT id, 'quiz', datetime('now', '-2 hours')
FROM groups 
WHERE name = 'Numbers';

-- Add some word reviews
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
SELECT w.id, s.id, true, datetime('now', '-1 day')
FROM words w
JOIN word_groups wg ON w.id = wg.word_id
JOIN study_sessions s ON wg.group_id = s.group_id
WHERE w.spanish IN ('hola', 'gracias');

INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
SELECT w.id, s.id, false, datetime('now', '-2 hours')
FROM words w
JOIN word_groups wg ON w.id = wg.word_id
JOIN study_sessions s ON wg.group_id = s.group_id
WHERE w.spanish = 'buenos días';
