SELECT u.id, username, registration_date,
(SELECT count(*) FROM question WHERE user_id = u.id) AS count_of_asked,
(SELECT COUNT(*) FROM answer WHERE user_id = u.id) AS count_of_answers,
(SELECT COUNT(*) FROM comment WHERE user_id = u.id) AS count_of_comments,
reputation
FROM users u
GROUP BY u.id
ORDER BY id