-- Connect to the database
--\c <put dbname here>;


CREATE TABLE GEOLOCATION (
    geolocation_zip_code_prefix VARCHAR(8) PRIMARY KEY,
    geolocation_lat NUMERIC(16,14),
    geolocation_lng NUMERIC(16,14),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(16)
);


CREATE TABLE PRODUCTS (
    product_id UUID PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER, --NOT NULL
    product_weight_g INTEGER, --NOT NULL
    product_length_cm INTEGER, --NOT NULL
    product_height_cm INTEGER, --NOT NULL
    product_width_cm INTEGER --NOT NULL
);


CREATE TABLE SELLERS (
    seller_id UUID PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(8),
    seller_city VARCHAR(100),
    seller_state VARCHAR(4),

    CONSTRAINT fk_sellers FOREIGN KEY (seller_zip_code_prefix) REFERENCES GEOLOCATION(geolocation_zip_code_prefix)
);

CREATE TABLE CUSTOMERS (
    customer_id UUID PRIMARY KEY,
    customer_unique_id UUID,
    customer_zip_code_prefix VARCHAR(8),
    customer_city VARCHAR(100),
    customer_state VARCHAR(4),

    CONSTRAINT fk_customers FOREIGN KEY (customer_zip_code_prefix) REFERENCES GEOLOCATION(geolocation_zip_code_prefix) 
);

CREATE TABLE ORDERS (
    order_id UUID PRIMARY KEY,
    customer_id UUID, --NOT NULL 
    order_status VARCHAR(32), --NOT NULL
    order_purchase_timestamp TIMESTAMP, --NOT NULL
    order_approved_at TIMESTAMP, --NOT NULL
    order_delivered_carrier_date TIMESTAMP, --NOT NULL
    order_delivered_customer_date TIMESTAMP, --NOT NULL
    order_estimated_delivery_date TIMESTAMP, --NOT NULL

    CONSTRAINT fk_orders FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

CREATE TABLE ORDER_PAYMENTS (
    order_id UUID, --NOT NULL
    payment_sequential INTEGER,
    payment_type VARCHAR(16), --NOT NULL
    payment_installments INTEGER,
    payment_value DECIMAL(19,6), --NOT NULL

    CONSTRAINT pk_order_payments PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT fk_order_payments FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

CREATE TABLE ORDER_REVIEWS (
    review_id UUID PRIMARY KEY,
    order_id UUID, --NOT NULL
    review_score INTEGER CHECK (review_score IN (1, 2, 3, 4, 5)), --NOT NULL 
    review_comment_title VARCHAR(256),
    review_comment_message VARCHAR(2048),
    review_creation_date TIMESTAMP, --NOT NULL
    review_answer_timestamp TIMESTAMP,

    CONSTRAINT fk_order_reviews FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

CREATE TABLE ORDER_ITENS (
    order_id UUID, --NOT NULL 
    order_item_id INTEGER,
    product_id UUID, --NOT NULL
    seller_id UUID, --NOT NULL
    shipping_limit_date TIMESTAMP, --NOT NULL
    price DECIMAL(19,6),
    freight_value DECIMAL(19,6),

    CONSTRAINT pk_order_itens PRIMARY KEY (order_id, order_item_id, product_id, seller_id),
    CONSTRAINT fk_order_itens_orders FOREIGN KEY (order_id) REFERENCES ORDERS(order_id),
    CONSTRAINT fk_order_itens_products FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id),
    CONSTRAINT fk_order_itens_sellers FOREIGN KEY (seller_id) REFERENCES SELLERS(seller_id)
);

CREATE TABLE PRODUCT_CATEGORY_NAME_TRANSLATION (
    product_category_name VARCHAR(64), 
    product_category_name_english VARCHAR(64), 

    CONSTRAINT pk_product_category_name PRIMARY KEY (product_category_name, product_category_name_english)
);

