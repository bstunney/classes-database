use neu;

DROP PROCEDURE IF EXISTS createClass; 
DELIMITER $$
CREATE PROCEDURE createClass(name VARCHAR(64), year VARCHAR(64), semester VARCHAR(64), grade VARCHAR(64), credits INT)
BEGIN
	INSERT INTO 
		class(name , year , semester , grade, credits)
	VALUES 
		(name , year , semester , grade, credits);
	END $$
	DELIMITER ;
    
CALL createClass("Calculus 3", "2022-2023", "Summer 2", "A-", 4);
SELECT * FROM class;

DROP PROCEDURE IF EXISTS readAllClass;
DELIMITER $$
CREATE PROCEDURE readAllClass()
BEGIN
    SELECT * FROM class;
END $$
DELIMITER ;

-- CALL readAllClass;

DROP PROCEDURE IF EXISTS updateGrade;
DELIMITER $$
CREATE PROCEDURE updateGrade (
n_name VARCHAR(64), n_grade VARCHAR(64))
BEGIN
	UPDATE class
	SET
    grade = n_grade WHERE name = n_name;
    
END $$
DELIMITER ;

-- CALL updateGrade("Calculus 3", "A");



DROP PROCEDURE IF EXISTS deleteClass;
DELIMITER $$
CREATE PROCEDURE deleteClass (n_name VARCHAR(64))
BEGIN
	DELETE FROM class
    WHERE name = n_name ;
END $$
DELIMITER ;

-- CALL deleteClass ("Calculus 3");

DROP PROCEDURE IF EXISTS readSemester;
DELIMITER $$
CREATE PROCEDURE readSemester(s_year VARCHAR(64), s_semester VARCHAR(64))
BEGIN

	SELECT * FROM class
		WHERE year = s_year AND semester = s_semester;
        
END $$
DELIMITER ;


-- CALL readSemester("2022-2023", "Summer 2");

SELECT semester from class;

