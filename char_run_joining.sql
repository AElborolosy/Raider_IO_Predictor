# database: 'raider_io_predictor'
# host: 'localhost'
# username: 'root'
# password: ''

/*
SQL Script That:
-Creates character_info and keystone_info tables.
-Loads data from character_info and keystone_info csvs into the tables.
-Indexes the tables.
-Inner Joins the tables and saves the result as a csv.

Create tables are stored here for reference if needed.
CREATE TABLE character_info (
	char_id int,
    score float
);

CREATE TABLE keystone_info_with_level (
	run_id int,
    run_score float,
    key_level int,
    run_time bigint,
    dungeon_name char(5),
    tank_id int,
    dps1_id int,
    dps2_id int,
    dps3_id int,
    healer_id int
);

# Load data from csv into the tables.
LOAD DATA LOCAL INFILE 'C:\\Users\\Ahmed\\PycharmProjects\\Raider_IO_Predictor\\data\\character_info.csv'
INTO TABLE character_info
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE 'C:\\Users\\Ahmed\\PycharmProjects\\Raider_IO_Predictor\\data\\keystone_run_info_with_level.csv'
INTO TABLE keystone_info_with_level
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

# Creat indexes for the character_info table.
ALTER TABLE character_info ADD PRIMARY KEY (char_id);
*/

# JOIN THE TWO TABLES TOGETHER.
SELECT
	'run_score',
    'run_time',
    'key_level',
    'dungeon_name',
    'tank_score',
    'dps1_score',
    'dps2_score',
    'dps3_score',
    'healer_score'
    FROM character_info
UNION
SELECT
	keystone_info_with_level.run_score,
    keystone_info_with_level.run_time,
    keystone_info_with_level.key_level,
    keystone_info_with_level.dungeon_name,
    tank_info.score AS tank_score,
    dps1_info.score AS dps1_score,
    dps2_info.score AS dps2_score,
    dps3_info.score AS dps3_score,
    healer_info.score AS healer_score
FROM keystone_info_with_level
INNER JOIN character_info AS tank_info ON keystone_info_with_level.tank_id = tank_info.char_id
INNER JOIN character_info AS dps1_info ON keystone_info_with_level.dps1_id = dps1_info.char_id
INNER JOIN character_info AS dps2_info ON keystone_info_with_level.dps2_id = dps2_info.char_id
INNER JOIN character_info AS dps3_info ON keystone_info_with_level.dps3_id = dps3_info.char_id
INNER JOIN character_info AS healer_info ON keystone_info_with_level.healer_id = healer_info.char_id
INTO OUTFILE 'C:\\Users\\Ahmed\\PycharmProjects\\Raider_IO_Predictor\\data\\joined_data_with_level.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';
