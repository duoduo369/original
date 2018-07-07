init db
---

    CREATE DATABASE IF NOT EXISTS original DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
    CREATE USER 'original'@'%' IDENTIFIED BY '123456'; # todo change password && username,
    GRANT ALL ON original.* TO 'original'@'%';
    flush privileges;
