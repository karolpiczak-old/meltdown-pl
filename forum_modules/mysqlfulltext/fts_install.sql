CREATE TABLE forum_mysqlftsindex (
	id int NOT NULL AUTO_INCREMENT,
	node_id int NOT NULL UNIQUE,
	body longtext NOT NULL,
	title varchar(300),
	tagnames varchar(255),
	PRIMARY KEY (id),
	FOREIGN KEY (node_id) REFERENCES forum_node (id)   ON UPDATE CASCADE ON DELETE CASCADE,
	FULLTEXT (body, title, tagnames),
	FULLTEXT(body),
	FULLTEXT(title),
	FULLTEXT(tagnames)
) ENGINE=`MyISAM`;

ALTER TABLE forum_mysqlftsindex CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

delimiter |

CREATE TRIGGER fts_on_insert AFTER INSERT ON forum_node
  FOR EACH ROW
  BEGIN
    INSERT INTO forum_mysqlftsindex (node_id, title, body, tagnames) VALUES (NEW.id, UPPER(NEW.title), UPPER(NEW.body), UPPER(NEW.tagnames));
  END;
|

delimiter |

CREATE TRIGGER fts_on_update AFTER UPDATE ON forum_node
  FOR EACH ROW
  BEGIN
    UPDATE forum_mysqlftsindex SET title = UPPER(NEW.title), body = UPPER(NEW.body), tagnames = UPPER(NEW.tagnames) WHERE node_id = NEW.id;
  END;

|

INSERT INTO forum_mysqlftsindex (node_id, title, body, tagnames) SELECT id, UPPER(title), UPPER(body), UPPER(tagnames) FROM forum_node;

