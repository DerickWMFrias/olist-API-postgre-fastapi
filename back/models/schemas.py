import uuid
from sqlalchemy import (
    String,
    Integer,
    Boolean, 
    DateTime,
    ForeignKey,
    Numeric,
    TIMESTAMP,
    CheckConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import UUID
from decimal import Decimal
from datetime import datetime
from dbconfig.base import Base as SQLAlchemyBase




class ProductCategoryNameTranslation(SQLAlchemyBase):
    __tablename__ = "product_category_name_translation"

    product_category_name: Mapped[str] = mapped_column(
        String(128),
        primary_key=True
    )

    product_category_name_english: Mapped[str] = mapped_column(
        String(128),
        nullable = False
    )

    #list, pois cada objeto/entidade daqui pode aparecer em muitos Products
    #relation_products: Mapped[list["Products"]] = relationship(
    #    back_populates="relation_category_name"
    #)


    def __repr__(self) -> str:
        return f"<ProductCategoryNameTranslation(product_category_name={self.product_category_name}, product_category_name_english={self.product_category_name_english})>"




class Geolocation(SQLAlchemyBase):
    __tablename__ = "geolocation"

    geolocation_zip_code_prefix: Mapped[str] = mapped_column(
        String(8),
        primary_key=True
    )

    geolocation_city: Mapped[str] = mapped_column(
        String(100)
    )

    geolocation_state: Mapped[str] = mapped_column(
        String(16)
    )


    """
    Estes campos a seguir definem relações unidirecionais com as tabelas que estejam entre "", como "Coordinates".

    Isto é uma das coisas poderosas do ORM, ao definir: 
        
    coordinates:Mapped[list["Coordinates"]] = ...

    estarei mostrando pro ORM que existe uma ligação entre essas tabelas, de forma que se eu tiver um objeto
    tal qual obj = Geolocation(), poderei acessar obj.coordinates para ver todas as coordenadas que tem a fk referenciando a 
    pk do meu obj.
    """

    relation_coordinates: Mapped[list["Coordinates"]] = relationship(
        back_populates="relation_geolocation"
    )
    relation_sellers: Mapped[list["Seller"]] = relationship(
        back_populates="relation_geolocation"
    )
    relation_customers: Mapped[list["Customer"]] = relationship(
        back_populates="relation_geolocation"
    )

    """
    relation_coordinates:Mapped[list["Coordinates"]] = ...  
    significa que esta row desta classe pode aparecer em diversas rows
    da tabela Coordinates (i.e, relação 1-n --> Desta c/Coordinates)

    relation_geolocation:Mapped["Geolocation"] = ...  
    significa que cada row desta classe referencia exatamente uma row
    da tabela Geolocation (i.e, relação 1-n --> Geolocation c/ Esta)
    """

    """
    Um ponto de atenção: Performance

    Embora seja muito prático, o acesso automático (geo.relation_coordinates) pode gerar o famoso problema de N+1 queries. 
    Se você carregar 100 geolocalizações e tentar acessar as coordenadas de cada uma em um loop, o SQLAlchemy fará:

        1 query inicial + 100 queries extras (uma para cada acesso à lista).
    """

    def __repr__(self) -> str:
        return f"<Geolocation(geolocation_zip_code_prefix={self.geolocation_zip_code_prefix}, geolocation_city={self.geolocation_city}, geolocation_state={self.geolocation_state})>"




class Coordinates(SQLAlchemyBase):
    __tablename__ = "coordinates"

    geolocation_zip_code_prefix: Mapped[str] = mapped_column(
        String(8),
        ForeignKey("geolocation.geolocation_zip_code_prefix")
    )

    lat: Mapped[Decimal] = mapped_column(
        Numeric(17, 14),
        primary_key=True
    )

    lng: Mapped[Decimal] = mapped_column(
        Numeric(17, 14),
        primary_key=True
    )

    #Sem list, pois cada Coordinate referencia exatamente uma Geolocation
    relation_geolocation: Mapped["Geolocation"] = relationship(
        back_populates="relation_coordinates"
    )

    def __repr__(self) -> str:
        return f"<Coordinates(geolocation_zip_code_prefix={self.geolocation_zip_code_prefix}, lat={self.lat}, lng={self.lng})>"






class Products(SQLAlchemyBase):
    __tablename__ = "products"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    product_category_name: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("product_category_name_translation.product_category_name")
    )

    product_name_lenght: Mapped[int | None] = mapped_column(
        Integer
    )

    product_description_lenght: Mapped[int | None] = mapped_column(
        Integer
    )

    product_photos_qty: Mapped[int | None] = mapped_column(
        Integer
    )

    product_weight_g: Mapped[int | None] = mapped_column(
        Integer
    )

    product_length_cm: Mapped[int | None] = mapped_column(
        Integer
    )

    product_height_cm: Mapped[int | None] = mapped_column(
        Integer
    )

    product_width_cm: Mapped[int | None] = mapped_column(
        Integer
    )

    relation_order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="relation_products"
    )

    #relation_category_name: Mapped["ProductCategoryNameTranslation"] = relationship(
    #    back_populates="relation_products"
    #)

    def __repr__(self) -> str:
        return f""





class Seller(SQLAlchemyBase):
    __tablename__ = "sellers"

    seller_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    seller_zip_code_prefix: Mapped[str] = mapped_column(
        String(8),
        ForeignKey("geolocation.geolocation_zip_code_prefix")
    )

    seller_city: Mapped[str] = mapped_column(String(100))
    seller_state: Mapped[str] = mapped_column(String(4))

    relation_geolocation: Mapped["Geolocation"] = relationship(
        back_populates="relation_sellers"
    )

    relation_order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="relation_sellers"
    )

    def __repr__(self) -> str:
        return f""






class Customer(SQLAlchemyBase):
    __tablename__ = "customers"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_unique_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    customer_zip_code_prefix: Mapped[str] = mapped_column(
        String(8),
        ForeignKey("geolocation.geolocation_zip_code_prefix")
    )

    customer_city: Mapped[str] = mapped_column(String(100))
    customer_state: Mapped[str] = mapped_column(String(4))

    relation_geolocation: Mapped["Geolocation"] = relationship(
        back_populates="relation_customers"
    )

    relation_orders: Mapped[list["Order"]] = relationship(
        back_populates="relation_customers"
    )

    def __repr__(self) -> str:
        return f""






class Order(SQLAlchemyBase):
    __tablename__ = "orders"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id")
    )

    order_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    order_purchase_timestamp: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP)
    order_approved_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP)
    order_delivered_carrier_date: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP)
    order_delivered_customer_date: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP)
    order_estimated_delivery_date: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP)

    relation_customers: Mapped["Customer"] = relationship(
        back_populates="relation_orders"
    )

    relation_order_payments: Mapped[list["OrderPayment"]] = relationship(
        back_populates="relation_orders"
    )

    relation_order_reviews: Mapped[list["OrderReview"]] = relationship(
        back_populates="relation_orders"
    )

    relation_order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="relation_orders"
    )


    def __repr__(self) -> str:
        return f""







class OrderPayment(SQLAlchemyBase):
    __tablename__ = "order_payments"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        primary_key=True
    )

    payment_sequential: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    payment_type: Mapped[str] = mapped_column(String(16), nullable=False)
    payment_installments: Mapped[int] = mapped_column(Integer, nullable=False)

    payment_value: Mapped[Decimal] = mapped_column(
        Numeric(19, 6),
        nullable=False
    )

    relation_orders: Mapped["Order"] = relationship(
        back_populates="relation_order_payments"
    )



    def __repr__(self) -> str:
        return f""




class OrderReview(SQLAlchemyBase):
    __tablename__ = "order_reviews"

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        nullable=False
    )

    review_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    review_comment_title: Mapped[str | None] = mapped_column(String(256))
    review_comment_message: Mapped[str | None] = mapped_column(String(2048))

    review_creation_date: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP)
    review_answer_timestamp: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP)

    __table_args__ = (
        CheckConstraint("review_score IN (1, 2, 3, 4, 5)", name="check_review_score"),
    )

    relation_orders: Mapped["Order"] = relationship(
        back_populates="relation_order_reviews"
    )


    def __repr__(self) -> str:
        return f""





class OrderItem(SQLAlchemyBase):
    __tablename__ = "order_items"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        primary_key=True
    )

    order_item_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.product_id"),
        primary_key=True
    )

    seller_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sellers.seller_id"),
        primary_key=True
    )

    shipping_limit_date: Mapped[TIMESTAMP | None] = mapped_column(
        TIMESTAMP
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(19, 6),
        nullable=False
    )

    freight_value: Mapped[Decimal | None] = mapped_column(
        Numeric(19, 6)
    )


    relation_orders: Mapped["Order"] = relationship(
        back_populates="relation_order_items"
    )

    relation_products: Mapped["Products"] = relationship(
        back_populates="relation_order_items"
    )

    relation_sellers: Mapped["Seller"] = relationship(
        back_populates="relation_order_items"
    )


    def __repr__(self) -> str:
        return f""







class User(SQLAlchemyBase):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    recovery_email: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    relation_keys: Mapped[list["Keys"]] = relationship(
        back_populates="relation_users",
        #cascade="all, delete-orphan"
    )


    def __repr__(self) -> str:
        return f""





class Keys(SQLAlchemyBase):
    __tablename__ = "keys"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False
    )

    key_text: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    expires_at_tmzone: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at_tmzone: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    relation_users: Mapped["User"] = relationship(
        back_populates="relation_keys"
    )


    def __repr__(self) -> str:
        return f""