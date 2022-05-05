# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order 
#     ==> done 22-02-17
#
#   * Make sure each model has one field with primary_key=True
#     ==> DjangoContentType
#         AuthUser
#         DjangoAdminLog
#         AuthPermission
#         AuthGroup 
#         => id = models.BigAutoField(primary_key=True) 추가
#
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#     ==> Change 'models.DO_NOTHING' to 'models.CASCADE'
#
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
#
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django_quill.fields import QuillField


class DjangoContentType(models.Model):
    id = models.BigAutoField(primary_key=True)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class AuthUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class DjangoAdminLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class AuthPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(DjangoContentType, models.CASCADE)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.CASCADE)
    permission = models.ForeignKey(AuthPermission, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)
    group = models.ForeignKey(AuthGroup, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)
    permission = models.ForeignKey(AuthPermission, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Membership(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    level = models.CharField(max_length=50, blank=True, null=True)
    condition = models.IntegerField(blank=True, null=True)
    acc_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membership'


class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    mem_name = models.CharField(max_length=100, blank=True, null=True)
    mem_phone = models.CharField(max_length=100, blank=True, null=True)
    mem_point = models.IntegerField(blank=True, null=True)
    monthtly_price = models.IntegerField(blank=True, null=True)
    mem_level = models.ForeignKey(Membership, models.CASCADE)
    user = models.OneToOneField(User, models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'



class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    member = models.ForeignKey(Member, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'cart'


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pay_method = models.CharField(max_length=50, blank=True, null=True)
    member = models.ForeignKey(Member, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'payment'


class ShopCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_category'
        

class Shop(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    shop_name = models.CharField(max_length=50, blank=True, null=True)
    shop_phone = models.CharField(max_length=50, blank=True, null=True)
    shop_category = models.ForeignKey(ShopCategory, models.CASCADE)
    manager = models.ForeignKey(Member, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'shop'



class ProCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pro_category'


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    stock = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pro_category = models.ForeignKey(ProCategory, models.CASCADE)
    shop = models.ForeignKey(Shop, models.CASCADE)
    content = QuillField(blank=True, null=True)
    main_img = models.ImageField(blank=True, null=True, upload_to='product/main')


    class Meta:
        managed = False
        db_table = 'product'


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    call = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    transport_no = models.CharField(max_length=50, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    order_no = models.CharField(max_length=50, blank=True, null=True)
    member = models.ForeignKey(Member, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'order'


class OrderProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    amount = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey(Order, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    status = models.CharField(max_length=50, blank=True, null=True)
    review_flag = models.CharField(max_length=10, blank=True, null=True, default='0')

    class Meta:
        managed = False
        db_table = 'order-product'


class Option(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    opt_name = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'option'

class CartProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(max_length=50, blank=True, null=True)
    cart = models.ForeignKey(Cart, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'cart-product'

class Liked(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    member = models.ForeignKey(Member, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'liked'

class LikedProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    liked = models.ForeignKey(Liked, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'liked-product'


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(blank=True, null=True)
    rate = models.CharField(max_length=50, blank=True, null=True)
    member = models.ForeignKey(Member, models.CASCADE)
    orderproduct = models.ForeignKey(OrderProduct, models.CASCADE)
    comment_img = models.ImageField(blank=True, null=True, upload_to='comment/main')
    reply_flag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'

class CommentReply(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=50, blank=True, null=True)
    comment = models.ForeignKey(Comment, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'comment_reply'



class QnaCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qna_category'

class Qna(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    member = models.ForeignKey(Member, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(QnaCategory, models.CASCADE)
    answer_flag = models.CharField(max_length=10, blank=True, null=True)
    qna_img = models.ImageField(blank=True, null=True, upload_to='qna/main')

    class Meta:
        managed = False
        db_table = 'qna'


class QnaAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(blank=True, null=True)
    qna = models.ForeignKey(Qna, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'qna_answer'


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleteflag = models.CharField(db_column='DeleteFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ad_name = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    ad_detail = models.CharField(max_length=50, blank=True, null=True)
    member = models.ForeignKey(Member, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'address'
