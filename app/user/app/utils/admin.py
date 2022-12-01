from sqladmin import ModelView

from orm.user import UserModel


class UserModelView(
    ModelView,
    model=UserModel,
):
    column_list = [
        UserModel.id,
        UserModel.telegram,
        UserModel.email,
        UserModel.registration_type,
        UserModel.join,
    ]
