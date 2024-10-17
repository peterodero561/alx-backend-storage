--
DELIMITER //

CREATE PROCEDURE AddBonus (
	IN user_id INT,
	IN project_name VARCHAR(255),
	IN score INT
)

BEGIN 
	DECLARE project_id INT DEFAULT NULL;

	-- CHECK if project exists
	SELECT id INTO project_id
	FROM projects
	WHERE name = project_name;

	-- if project does not exist insert it
	IF project_id IS NULL THEN
		INSERT INTO projects (name) VALUES (project_name);
		SET project_id = LAST_INSERT_ID();
	END IF;

	-- INSERT into correction into corrections table
	INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END; //
DELIMITER ;
