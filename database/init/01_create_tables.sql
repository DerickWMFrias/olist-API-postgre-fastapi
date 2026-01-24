-- Connect to the database
--\c <put dbname here>;


CREATE TABLE PRODUCT_CATEGORY_NAME_TRANSLATION (
    product_category_name VARCHAR(128), 
    product_category_name_english VARCHAR(128) NOT NULL, 

    CONSTRAINT pk_product_category_name PRIMARY KEY (product_category_name)
);


CREATE TABLE GEOLOCATION (
    geolocation_zip_code_prefix VARCHAR(8) PRIMARY KEY,
    geolocation_city VARCHAR(100) NOT NULL,
    geolocation_state VARCHAR(16) NOT NULL
);


CREATE TABLE COORDINATES (
    coordinate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    geolocation_zip_code_prefix VARCHAR(8),
    lat NUMERIC(17,14),
    lng NUMERIC(17,14),

    CONSTRAINT unique_coordinates UNIQUE (lat, lng),
    CONSTRAINT fk_coordinates FOREIGN KEY (geolocation_zip_code_prefix) REFERENCES GEOLOCATION(geolocation_zip_code_prefix) ON DELETE CASCADE
);


CREATE TABLE PRODUCTS (
    product_id UUID PRIMARY KEY,
    product_category_name VARCHAR(128),
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER

    -- CONSTRAINT fk_products FOREIGN KEY (product_category_name) REFERENCES PRODUCT_CATEGORY_NAME_TRANSLATION(product_category_name)
);


CREATE TABLE SELLERS (
    seller_id UUID PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(8),
    seller_city VARCHAR(100) NOT NULL,
    seller_state VARCHAR(4) NOT NULL,

    CONSTRAINT fk_sellers FOREIGN KEY (seller_zip_code_prefix) REFERENCES GEOLOCATION(geolocation_zip_code_prefix)
);

CREATE TABLE CUSTOMERS (
    customer_id UUID PRIMARY KEY,
    customer_unique_id UUID NOT NULL,
    customer_zip_code_prefix VARCHAR(8),
    customer_city VARCHAR(100) NOT NULL,
    customer_state VARCHAR(4) NOT NULL,

    CONSTRAINT fk_customers FOREIGN KEY (customer_zip_code_prefix) REFERENCES GEOLOCATION(geolocation_zip_code_prefix) 
);

CREATE TABLE ORDERS (
    order_id UUID PRIMARY KEY,
    customer_id UUID,
    order_status VARCHAR(32) NOT NULL,
    order_purchase_timestamp TIMESTAMP, 
    order_approved_at TIMESTAMP, 
    order_delivered_carrier_date TIMESTAMP, 
    order_delivered_customer_date TIMESTAMP, 
    order_estimated_delivery_date TIMESTAMP, 

    CONSTRAINT fk_orders FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

CREATE TABLE ORDER_PAYMENTS (
    order_id UUID,
    payment_sequential INTEGER,
    payment_type VARCHAR(16) NOT NULL,
    payment_installments INTEGER NOT NULL,
    payment_value NUMERIC(19,6) NOT NULL,

    CONSTRAINT pk_order_payments PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT fk_order_payments FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

CREATE TABLE ORDER_REVIEWS (
    review_id UUID PRIMARY KEY,
    order_id UUID,
    review_score INTEGER CHECK (review_score IN (1, 2, 3, 4, 5)) NOT NULL, 
    review_comment_title VARCHAR(256),
    review_comment_message VARCHAR(2048),
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,

    CONSTRAINT fk_order_reviews FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

CREATE TABLE ORDER_ITEMS (
    order_id UUID,  
    order_item_id INTEGER,
    product_id UUID, 
    seller_id UUID, 
    shipping_limit_date TIMESTAMP, 
    price NUMERIC(19,6) NOT NULL,
    freight_value NUMERIC(19,6),

    CONSTRAINT pk_order_items PRIMARY KEY (order_id, order_item_id, product_id, seller_id),
    CONSTRAINT fk_order_items_orders FOREIGN KEY (order_id) REFERENCES ORDERS(order_id),
    CONSTRAINT fk_order_items_products FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id),
    CONSTRAINT fk_order_items_sellers FOREIGN KEY (seller_id) REFERENCES SELLERS(seller_id)
);



CREATE TABLE USERS(
    user_id UUID DEFAULT gen_random_uuid(),
    email VARCHAR(128) NOT NULL UNIQUE,
    hashed_password VARCHAR(128) NOT NULL,
    recovery_email VARCHAR(128) NOT NULL,

    CONSTRAINT pk_users PRIMARY KEY (user_id)
);

CREATE TABLE KEYS(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    key_text UUID NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE NOT NULL,
    expires_at_tmzone TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at_tmzone TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    CONSTRAINT fk_keys_users FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
);