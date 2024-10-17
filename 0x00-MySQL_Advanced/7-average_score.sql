--
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id)

BEGIN
	DECLARE average_score FLOAT

	SELECT AVG(score) INTO average_score
	FROM corrections
	WHERE user_id = user_id;

	IF EXISTS (SELECT 1 FROM users WHERE user_id = user_id) THEN
		UPDATE users
		set average_score = average_score
		WHERE user_id = user_id;
	ELSE
		INSERT INTO users (id, average_score) VALUES (user_id, average_score)
	END IF
END //
DELIMITER ;
