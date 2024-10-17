--
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE userID INT;
    DECLARE weighted_avg FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE total_score FLOAT DEFAULT 0;

    -- Declare a cursor to iterate over all users
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET userID = NULL;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through all users
    read_loop: LOOP
        FETCH user_cursor INTO userID;

        -- Exit the loop if no more users
        IF userID IS NULL THEN
            LEAVE read_loop;
        END IF;

        -- Compute the weighted average score for the current user
        SELECT 
            IFNULL(SUM(c.score * p.weight), 0) AS total_score,
            IFNULL(SUM(p.weight), 0) AS total_weight
        INTO total_score, total_weight
        FROM corrections c
        LEFT JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = userID;

        -- Avoid dividing by 0
        IF total_weight > 0 THEN
            SET weighted_avg = total_score / total_weight;
        ELSE
            SET weighted_avg = 0;
        END IF;

        -- Update the user's average_score in the users table
        UPDATE users
        SET average_score = weighted_avg
        WHERE id = userID;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END //
DELIMITER ;
