-- =============================================
-- Читальня: SQL-запросы проекта
-- =============================================

-- 1. Список всех источников
SELECT id, title, author, year, type
FROM sources
ORDER BY title;

-- 2. Список всех списков литературы с владельцами
SELECT reading_lists.id, reading_lists.title, users.full_name AS owner_name
FROM reading_lists
JOIN users ON reading_lists.owner_id = users.id
ORDER BY reading_lists.title;

-- 3. Источники заданного типа (WHERE)
SELECT id, title, author, year
FROM sources
WHERE type = ?
ORDER BY title;

-- 4. Источники, изданные не ранее заданного года (WHERE)
SELECT id, title, author, year
FROM sources
WHERE year >= ?
ORDER BY year DESC;

-- 5. Поиск источников по подстроке в названии или авторе (WHERE LIKE)
SELECT id, title, author, year, type
FROM sources
WHERE title LIKE ? OR author LIKE ?
ORDER BY title;

-- 6. Элементы списка с информацией об источнике и категории (JOIN)
SELECT reading_list_items.id,
       sources.title AS source_title,
       sources.author AS source_author,
       categories.name AS category_name,
       reading_list_items.status
FROM reading_list_items
JOIN sources ON reading_list_items.source_id = sources.id
LEFT JOIN categories ON reading_list_items.category_id = categories.id
WHERE reading_list_items.reading_list_id = ?
ORDER BY sources.title;

-- 7. Общее количество источников (агрегат COUNT)
SELECT COUNT(*) AS sources_count FROM sources;

-- 8. Количество прочитанных источников (агрегат COUNT)
SELECT COUNT(*) AS completed_count
FROM reading_list_items
WHERE status = 'прочитан';

-- 9. Количество источников по типам (GROUP BY)
SELECT type, COUNT(*) AS count
FROM sources
GROUP BY type
ORDER BY count DESC;

-- 10. Количество элементов в каждом списке (GROUP BY + JOIN)
SELECT reading_lists.id, reading_lists.title,
       COUNT(reading_list_items.id) AS items_count
FROM reading_lists
LEFT JOIN reading_list_items
    ON reading_list_items.reading_list_id = reading_lists.id
GROUP BY reading_lists.id, reading_lists.title
ORDER BY items_count DESC;

-- 11. Категории с числом источников не менее заданного (GROUP BY + HAVING)
SELECT categories.name, COUNT(category_sources.source_id) AS count
FROM categories
LEFT JOIN category_sources
    ON category_sources.category_id = categories.id
GROUP BY categories.id, categories.name
HAVING COUNT(category_sources.source_id) >= ?
ORDER BY count DESC;

-- 12. Источники в заданной категории (JOIN)
SELECT sources.id, sources.title, sources.author, sources.year
FROM sources
JOIN category_sources ON category_sources.source_id = sources.id
WHERE category_sources.category_id = ?
ORDER BY sources.title;