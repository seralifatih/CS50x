-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = "Chamberlin Street"; --this query is the start from the initial available information and leads to the interview transcripts of three witneses

SELECT transcript FROM interviews WHERE month = 7 AND day = 28; -- according to the transcripts the thief got in a c
--ar within 10 minutes of the theft (10:15am)
--security footage from that time to the parking lot might show something
--this was withdrawing money from the ATM at Fifer Street in the morning of the theft
--thief plans to leave Fiftyville tomorrow with the earliest flight

SELECT license_plate, activity, hour, minute FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour = 10; --parking lot security log

SELECT name, passport_number, license_plate FROM people
WHERE id IN (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw"));
--names, passport number and license plates of those who withdrew money from Fifer STreet on the day of crime

SELECT license_plate FROM courthouse_security_logs
WHERE license_plate IN (SELECT license_plate FROM people
WHERE id IN (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw")))
and activity = "exit" AND minute < 25 AND minute > 15;
--plate numbers of the people who withdrew money  at the atm and used parking space. they are the primary suspects

SELECT phone_number FROM people WHERE license_plate IN (SELECT DISTINCT(license_plate) FROM courthouse_security_logs
WHERE license_plate IN (SELECT license_plate FROM people
WHERE id IN (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw")))
AND activity = "exit" AND minute < 25 AND minute > 15);
--phone numbers of suspects


SELECT DISTINCT(caller) FROM phone_calls WHERE caller IN (SELECT phone_number FROM people
WHERE license_plate IN (SELECT DISTINCT(license_plate) FROM courthouse_security_logs
WHERE license_plate IN (SELECT license_plate FROM people
WHERE id IN (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw")))
AND activity = "exit" AND minute < 25 AND minute > 15)) AND duration < 60;
--thieves' phone number as we know the duration was less than a minute

SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE caller IN (SELECT phone_number FROM people
WHERE license_plate IN (SELECT DISTINCT(license_plate) FROM courthouse_security_logs
WHERE license_plate IN (SELECT license_plate FROM people
WHERE id IN (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw")))
AND activity = "exit" AND minute < 25 AND minute > 15)) AND duration < 60);
--primary suspect list


SELECT city FROM airports
WHERE id = (SELECT destination_airport_id FROM flights
WHERE origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville")
AND month = 7 AND day = 29 AND year = 2020 ORDER BY hour LIMIT 1); --first flight next day is to London


SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights
WHERE origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville")
AND month = 7 AND day = 29 AND year = 2020 ORDER BY hour LIMIT 1); --passport numbers of people leaving with the first flight


SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE caller IN (SELECT phone_number FROM people
WHERE license_plate IN (SELECT DISTINCT(license_plate) FROM courthouse_security_logs
WHERE license_plate IN (SELECT license_plate FROM people
WHERE id IN (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw")))
AND activity = "exit" AND minute < 25 AND minute > 15)) AND duration < 60)
INTERSECT
SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights
WHERE origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville")
AND month = 7 AND day = 29 AND year = 2020 ORDER BY hour LIMIT 1)); --primary suspect is Ernest



SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE passport_number IN (SELECT passport_number FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE caller IN (SELECT phone_number FROM people
WHERE license_plate IN (SELECT DISTINCT(license_plate) FROM courthouse_security_logs
WHERE license_plate IN (SELECT license_plate FROM people
WHERE id IN (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw")))
AND activity = "exit" AND minute < 25 AND minute > 15)) AND duration < 60)
INTERSECT
SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights
WHERE origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville")
AND month = 7 AND day = 29 AND year = 2020 ORDER BY hour LIMIT 1))) AND duration < 60 AND month = 7 AND day = 28 AND year = 2020);
--name of accomplice Berthold

