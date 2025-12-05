from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.theme import Bootstrap4Theme
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect
from saleapp2025 import app, db
from models import Category, Product, User, UserEnum
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        # Kiểm tra xem thẻ HTML đã có class nào chưa
        if kwargs.get('class'):
            # Nếu có rồi, nối thêm class 'ckeditor' vào
            kwargs['class'] += ' ckeditor'
        else:
            # Nếu chưa, đặt class mặc định là 'ckeditor'
            kwargs.setdefault('class', 'ckeditor')

        # Trả về mã HTML chuẩn của TextArea nhưng đã kèm class mới
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


# 2. Định nghĩa Field (Logic xử lý dữ liệu)
class CKTextAreaField(TextAreaField):
    # Gắn Widget đã tạo ở trên vào Field này
    widget = CKTextAreaWidget()

class AuthenticatedModelView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated #and current_user.role == UserEnum.ADMIN

class MyCategoryView(AuthenticatedModelView):
    column_list = ["name","products"]
    column_searchable_list = ["name"]
    column_filters = ["name"]
    column_labels = {
        "name": "Tên loại",
        "products": "Danh sách sản phẩm"
    }

class MyProductView(AuthenticatedModelView):
    column_list = ["name","price","category","image","description"]
    column_searchable_list = ["name"]
    column_filters = ["name"]
    column_labels = {
        "name": "Tên sản phẩm",
        "image": "Ảnh",
        "price": "Giá",
        "cate_id": "Mã loại"
    }
    can_export = True
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        "description": CKTextAreaField
    }

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self) -> str:
        return self.render("admin/index.html")

class MyAdminLogoutView(BaseView):
    @expose("/")
    def index(self) -> str:
        logout_user()
        return redirect("/admin")
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose("/")
    def index(self) -> str:
        return self.render("admin/stats.html")

admin = Admin(app=app,name="E-COMMERCE", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyAdminLogoutView("ĐĂNG XUẤT"))
admin.add_view(StatsView("THỐNG KÊ"))