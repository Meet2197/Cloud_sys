
INSERT INTO files (id, name, type, metadata, created_at)
VALUES
(1, 'welcome.txt', 'text', '{"description": "Hello world"}', CURRENT_TIMESTAMP),
(2, 'sample.png', 'image', '{"resolution": "1024x768"}', CURRENT_TIMESTAMP),
(3, 'dataset.json', 'json', '{"records": 100}', CURRENT_TIMESTAMP);
