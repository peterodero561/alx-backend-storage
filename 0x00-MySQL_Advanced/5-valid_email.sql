-- script that creates a trigger that resets the attribute valid_email only when the email has been changed.
DELIMITER //
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
	-- CHECK if email was changed
	IF NEW.email != OLD.email THEN
		SET NEW.valid_email = FALSE;
	END IF;
END; //
DELIMITER //
