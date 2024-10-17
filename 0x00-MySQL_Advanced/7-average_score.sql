--
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (IN input_id INT)

BEGIN
	DECLARE average_score FLOAT;

	SELECT AVG(score) INTO average_score
	FROM corrections
	WHERE user_id = input_id;

	IF EXISTS (SELECT 1 FROM users WHERE id = input_id) THEN
		UPDATE users
		set average_score = average_score
		WHERE id = input_id;
	ELSE
		INSERT INTO users (id, average_score) VALUES (input_id, average_score);
	END IF;
END //
DELIMITER ;
