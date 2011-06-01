DROP TRIGGER `fts_on_insert`;
DROP TRIGGER `fts_on_update`;

ALTER TABLE forum_mysqlftsindex ADD COLUMN title varchar(300) NOT NULL, ADD COLUMN tagnames varchar(255) NOT NULL;
ALTER TABLE forum_mysqlftsindex ENGINE = MYISAM;
ALTER TABLE forum_mysqlftsindex ADD FULLTEXT `title`(title), ADD FULLTEXT `tagnames`(tagnames);
UPDATE forum_mysqlftsindex ind JOIN forum_node node ON ind.node_id = node.id SET ind.body = UPPER(node.body), ind.title = UPPER(node.title), ind.tagnames = UPPER(node.tagnames);

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

delimiter |

ALTER TABLE forum_mysqlftsindex ADD FULLTEXT(body);
ALTER TABLE forum_mysqlftsindex ADD FULLTEXT(title);
ALTER TABLE forum_mysqlftsindex ADD FULLTEXT(tagnames);

|