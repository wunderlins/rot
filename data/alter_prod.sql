ALTER TABLE `planoaa`.`rotation` CHANGE COLUMN `rtyp` `rtyp` INT(11) NULL DEFAULT NULL  ;
ALTER TABLE `planoaa`.`rot_erfahrung` ADD COLUMN `typ` VARCHAR(45) NULL AFTER `pid`;

