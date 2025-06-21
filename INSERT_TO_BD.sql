-- Вставка стран
INSERT INTO bookstore_country (name) VALUES
('Россия'),
('США'),
('Великобритания'),
('Германия'),
('Франция');

-- Вставка городов
INSERT INTO bookstore_city (name, country_id) VALUES
('Москва', 1),
('Санкт-Петербург', 1),
('Нью-Йорк', 2),
('Лондон', 3),
('Берлин', 4),
('Париж', 5);

-- Вставка авторов
INSERT INTO bookstore_author (name, biography) VALUES
('Лев Толстой', 'Русский писатель, классик мировой литературы'),
('Федор Достоевский', 'Русский писатель, мыслитель, философ'),
('Антон Чехов', 'Русский писатель, драматург'),
('Джордж Оруэлл', 'Английский писатель и публицист'),
('Эрнест Хемингуэй', 'Американский писатель, журналист'),
('Франц Кафка', 'Немецкоязычный писатель');

-- Вставка издательств
INSERT INTO bookstore_publisher (name, description) VALUES
('АСТ', 'Крупнейшее российское издательство'),
('Эксмо', 'Одно из крупнейших издательств России'),
('Просвещение', 'Старейшее учебное издательство России'),
('Penguin Books', 'Британское издательство'),
('Random House', 'Американское издательство');

-- Вставка жанров
INSERT INTO bookstore_genre (name, description) VALUES
('Роман', 'Крупное повествовательное произведение'),
('Детектив', 'Произведение, посвященное раскрытию загадочного преступления'),
('Фантастика', 'Жанр литературы, описывающий вымышленные события'),
('Классика', 'Произведения, признанные образцовыми'),
('Поэзия', 'Стихотворные произведения');

-- Вставка книг
INSERT INTO bookstore_book (title, description, price, isbn, publication_date, pages, cover_image, stock_quantity, language) VALUES
('Война и мир', 'Роман-эпопея Льва Толстого', 1200.00, '9785171234567', '1869-01-01', 1225, 'https://example.com/war_and_peace.jpg', 50, 'Русский'),
('Преступление и наказание', 'Роман Федора Достоевского', 800.00, '9785171234568', '1866-01-01', 671, 'https://example.com/crime_and_punishment.jpg', 30, 'Русский'),
('1984', 'Антиутопический роман Джорджа Оруэлла', 600.00, '9785171234569', '1949-01-01', 328, 'https://example.com/1984.jpg', 25, 'Русский'),
('Старик и море', 'Повесть Эрнеста Хемингуэя', 400.00, '9785171234570', '1952-01-01', 127, 'https://example.com/old_man_and_sea.jpg', 40, 'Русский'),
('Процесс', 'Роман Франца Кафки', 550.00, '9785171234571', '1925-01-01', 255, 'https://example.com/trial.jpg', 20, 'Русский');

-- Связи книг с авторами
INSERT INTO bookstore_bookauthor (book_id, author_id) VALUES
(1, 1), -- Война и мир - Толстой
(2, 2), -- Преступление и наказание - Достоевский
(3, 4), -- 1984 - Оруэлл
(4, 5), -- Старик и море - Хемингуэй
(5, 6); -- Процесс - Кафка

-- Связи книг с издательствами
INSERT INTO bookstore_bookpublisher (book_id, publisher_id) VALUES
(1, 1), -- Война и мир - АСТ
(2, 2), -- Преступление и наказание - Эксмо
(3, 4), -- 1984 - Penguin Books
(4, 5), -- Старик и море - Random House
(5, 1); -- Процесс - АСТ

-- Связи книг с жанрами
INSERT INTO bookstore_bookgenre (book_id, genre_id) VALUES
(1, 1), -- Война и мир - Роман
(1, 4), -- Война и мир - Классика
(2, 1), -- Преступление и наказание - Роман
(2, 4), -- Преступление и наказание - Классика
(3, 3), -- 1984 - Фантастика
(4, 1), -- Старик и море - Роман
(5, 1); -- Процесс - Роман

-- Создание тестового пользователя (пароль: test123)
INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES ('pbkdf2_sha256$600000$test123$test123', NULL, false, 'testuser', 'Test', 'User', 'test@example.com', false, true, CURRENT_TIMESTAMP);

-- Создание адреса для тестового пользователя
INSERT INTO bookstore_address (user_id, country_id, city_id, street, postal_code)
VALUES (1, 1, 1, 'ул. Примерная, д. 1', '123456');

-- Создание корзины для тестового пользователя
INSERT INTO bookstore_cart (user_id, creation_date, last_update_date)
VALUES (1, CURRENT_DATE, CURRENT_DATE);

-- Добавление книг в корзину
INSERT INTO bookstore_cartitem (cart_id, book_id, quantity)
VALUES (1, 1, 2), -- 2 экземпляра "Война и мир"
       (1, 2, 1); -- 1 экземпляр "Преступление и наказание"

-- Создание заказа
INSERT INTO bookstore_order (user_id, total_price, status, address_id, order_date)
VALUES (1, 2000.00, 'PENDING', 1, CURRENT_DATE);

-- Добавление книг в заказ
INSERT INTO bookstore_orderitem (order_id, book_id, quantity, price_at_order_time)
VALUES (1, 1, 1, 1200.00), -- 1 экземпляр "Война и мир"
       (1, 3, 1, 600.00);  -- 1 экземпляр "1984"

-- Добавление отзывов
INSERT INTO bookstore_review (user_id, book_id, rating, comment, review_date)
VALUES (1, 1, 5, 'Отличная книга!', CURRENT_DATE),
       (1, 2, 4, 'Очень интересное произведение', CURRENT_DATE); 