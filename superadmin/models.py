import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import AbstractUser


# =========================================================
# ABSTRACT USER MODEL
# =========================================================

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

# =========================================================
# BASE MODEL
# =========================================================

class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# =========================================================
# CATEGORY
# =========================================================

class Category(BaseModel):
    name = models.CharField(max_length=255)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    meta_title = models.CharField(
        max_length=255,
        blank=True
    )

    meta_description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# BRAND
# =========================================================

class Brand(BaseModel):
    name = models.CharField(max_length=255)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    logo = models.ImageField(
        upload_to='brands/',
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# TAG
# =========================================================

class Tag(BaseModel):
    name = models.CharField(max_length=100)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# PRODUCT
# =========================================================

class Product(BaseModel):

    PRODUCT_TYPES = (
        ('physical', 'Physical'),
        ('digital', 'Digital'),
        ('service', 'Service'),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    short_description = models.TextField(blank=True)

    description = models.TextField(blank=True)

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES,
        default='physical'
    )

    thumbnail = models.ImageField(
        upload_to='products/thumbnails/',
        null=True,
        blank=True
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    meta_title = models.CharField(
        max_length=255,
        blank=True
    )

    meta_description = models.TextField(blank=True)

    warranty_information = models.TextField(blank=True)

    return_policy = models.TextField(blank=True)

    is_featured = models.BooleanField(default=False)

    is_digital = models.BooleanField(default=False)

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    total_reviews = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_featured']),
        ]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# PRODUCT ATTRIBUTE
# =========================================================

class Attribute(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AttributeValue(BaseModel):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name='values'
    )

    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name} - {self.value}"


# =========================================================
# PRODUCT VARIANT
# =========================================================

class ProductVariant(BaseModel):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    barcode = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    attributes = models.ManyToManyField(
        AttributeValue,
        blank=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    stock = models.IntegerField(default=0)

    low_stock_threshold = models.IntegerField(default=5)

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    tax_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['product__name']

    def __str__(self):
        return f"{self.product.name} - {self.sku}"


# =========================================================
# PRODUCT IMAGES
# =========================================================

class ProductImage(BaseModel):

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='products/images/'
    )

    is_primary = models.BooleanField(default=False)

    alt_text = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return self.variant.sku


# =========================================================
# ADDRESS
# =========================================================

class Address(BaseModel):

    ADDRESS_TYPES = (
        ('home', 'Home'),
        ('office', 'Office'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    full_name = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    address_line_1 = models.CharField(max_length=255)

    address_line_2 = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=20)

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES
    )

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


# =========================================================
# CART
# =========================================================

class Cart(BaseModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    def __str__(self):
        return str(self.user)


class CartItem(BaseModel):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.variant.sku


# =========================================================
# WISHLIST
# =========================================================

class Wishlist(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user} - {self.product.name}"


# =========================================================
# COUPON
# =========================================================

class Coupon(BaseModel):

    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    maximum_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    usage_limit = models.IntegerField(default=1)

    used_count = models.IntegerField(default=0)

    valid_from = models.DateTimeField()

    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code


# =========================================================
# ORDER
# =========================================================

class Order(BaseModel):

    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    order_number = models.CharField(
        max_length=100,
        unique=True
    )

    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name='shipping_orders'
    )

    billing_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name='billing_orders'
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    shipping_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    tracking_number = models.CharField(
        max_length=255,
        blank=True
    )

    shipping_partner = models.CharField(
        max_length=255,
        blank=True
    )

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number


# =========================================================
# ORDER ITEM
# =========================================================

class OrderItem(BaseModel):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True
    )

    product_name = models.CharField(max_length=255)

    sku = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.product_name


# =========================================================
# PAYMENT
# =========================================================

class Payment(BaseModel):

    PAYMENT_METHODS = (
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('paypal', 'Paypal'),
        ('cod', 'Cash On Delivery'),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    is_paid = models.BooleanField(default=False)

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    response_data = models.JSONField(
        default=dict,
        blank=True
    )

    def __str__(self):
        return self.payment_method


# =========================================================
# REVIEW
# =========================================================

class Review(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField()

    review = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return self.product.name