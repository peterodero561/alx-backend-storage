--
CREATE VIEW need_meeting AS
SELECT s.name
FROM students s
WHERE s.score < 80
AND (last_meeting IS NULL OR last_meeting < DATE_SUB(CURDATE(), INTERVAL 1 MONTH));
