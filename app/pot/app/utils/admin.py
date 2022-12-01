from sqladmin import ModelView

from orm.pot import PotModel


class PotModelView(
    ModelView,
    model=PotModel,
):
    column_list = [
        PotModel.id,
        PotModel.user_id,
        PotModel.pot,
    ]
