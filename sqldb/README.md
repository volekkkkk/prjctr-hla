### SELECT speed with different indexes

| Query                                                                                               | Without index          | BTREE | HASH |
|:---------------------------------------------------------------------------------------------------:|:----------------------:|:-----:|:----:|
|select SQL_NO_CACHE count(*) from USERS where birth_date < "2000-01-01"                              |                  15.57 | 8.54  |     -|
|select SQL_NO_CACHE count(*) from USERS where birth_date < "2005-01-01" and birth_date > "1990-01-01"|                  16.54 | 6.65  |     -|
|select SQL_NO_CACHE count(*) from USERS where birth_date > "1992-01-01"                              |                  14.68 | 10.25 |     -|

Hash index note - https://dev.mysql.com/doc/refman/8.0/en/innodb-adaptive-hash.html

### INSERT speed with different innodb_flush_log_at_trx_commit value
#### JMeter configuration
Number of threads (users): 250
Ramp-up period (seconds): 5
Duration (seconds): 60

| innodb_flush_log_at_trx_commit | Rows inserted |
|:------------------------------:|:-------------:|
| 0                              | 1,037,931     |
| 1                              | 978,323       |
| 2                              | 1,004,157     | 

