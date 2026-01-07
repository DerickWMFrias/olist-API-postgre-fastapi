-- VALID TOKENS 

INSERT INTO KEYS(user_id, key_text, is_revoked, expires_at_tmzone) 
VALUES('f7d6e87b-4221-4f11-9252-87611e3b5e1b',
       'd149023c-f5e2-4781-9b12-9c9876214563', FALSE, '2027-12-29 14:30:00+00');

INSERT INTO KEYS(user_id, key_text, is_revoked, expires_at_tmzone) 
VALUES('f7d6e87b-4221-4f11-9252-87611e3b5e1b', 
       'e1f2a3b4-c5d6-4789-8012-34567890abcd', FALSE, '2027-12-29 14:30:00+00');

INSERT INTO KEYS(user_id, key_text, is_revoked, expires_at_tmzone) 
VALUES('f7d6e87b-4221-4f11-9252-87611e3b5e1b', 
       '8e7d6c5b-4a3b-4210-9f8e-7d6c5b4a3b21', FALSE, '2027-12-29 14:30:00+00');

INSERT INTO KEYS(user_id, key_text, is_revoked, expires_at_tmzone) 
VALUES('9e6d8a34-2b1f-4318-8671-502a3a5f7082', 
       '2c1b0a98-7d6c-4b5a-4321-0e9d8c7b6a54', FALSE, '2027-12-29 14:30:00+00');

INSERT INTO KEYS(user_id, key_text, is_revoked, expires_at_tmzone) 
VALUES('9e6d8a34-2b1f-4318-8671-502a3a5f7082', 
       'c5b4a3b2-10e9-4d8c-7b6a-543210e9d8c7', FALSE, '2027-12-29 14:30:00+00');

INSERT INTO KEYS(user_id, key_text, is_revoked, expires_at_tmzone) 
VALUES('a32e1967-8974-4b47-9759-4560738e4112', 
       '0e9d8c7b-6a54-4321-0e9d-8c7b6a543210', FALSE, '2027-12-29 14:30:00+00');



-- INVALID KEYS


INSERT INTO KEYS(user_id, key_text, is_revoked, expires_at_tmzone, created_at_tmzone) 
VALUES('f7d6e87b-4221-4f11-9252-87611e3b5e1b', 
       '892095f9-0351-460d-a342-a892787c805a', TRUE, '2024-12-29 14:30:00+00', '2023-12-29 14:30:00+00');


INSERT INTO KEYS(user_id, key_text, is_revoked, expires_at_tmzone, created_at_tmzone) 
VALUES('67b2d56a-12e8-4993-9c54-46702e1b854a', 
       '52680654-e07b-40f4-8848-038c35581896', FALSE, '2024-12-29 14:30:00+00', '2023-12-29 14:30:00+00');


