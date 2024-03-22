-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street'
select * from interviews where year = 2021 and month = 7 and day = 28;
.schema bakery_security_logs
Select * FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 and 30;
select name from people where license_plate in (select license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 and 30);
select * from atm_transactions where year = 2021 and month = 7 and day = 28 and atm_location = 'Leggett Street' and transaction_type = 'withdraw';
select person_id from bank_accounts where account_number in
   ...> (select account_number from atm_transactions where year = 2021 and month = 7 and day = 28 and atm_location = 'Leggett Street' and transaction_type = 'withdraw');
   select * from flights where year = 2021 and month = 7 and day = 29;
   select passport_number from passengers where flight_id = 36;
   select name from people where passport_number in (select passport_number from passengers where flight_id = 36);
   select phone_number from people where name in (select name from people where passport_number in (select passport_number from passengers where flight_id = 36));
   select name, phone_number from people where name in ('Luca', 'Bruce');
   select name from people where phone_number in( select receiver from phone_calls where caller in (select phone_number from people where name in ('Luca', 'Bruce')) and year = 2021 and month = 7 and day = 28);
   select name, phone_number from people where name in('Gregory', 'Carl', 'Robin', 'Deborah');
