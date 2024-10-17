--
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)

BEGIN
	DECLARE weighted_avg FLOAT DEFAULT 0;
	DECLARE total_weight FLOAT DEFAULT 0;

	-- compute total weight score and total weight
	SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
	INTO weighted_avg, total_weight
	FROM corrections
	INNER JOIN projects ON  corrections.project_id = projects.id
	WHERE corrections.user_id = user_id;

	-- avoid dividing by 0
	IF total_weight > 0 THEN
		SET weighted_avg = weighted_avg / total_weight;
	ELSE
		SET weighted_avg = 0;
	END IF;

	-- UPDATE USERS
	UPDATE users
	SET average_score = weighted_avg
	WHERE id = user_id;
END //
DELIMITER ;
