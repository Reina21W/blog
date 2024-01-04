import wtforms
from wtforms.validators import Email, EqualTo, Length, InputRequired
from models import UserModel


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Wrong Format!")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="Wrong username!")])
    Password1 = wtforms.StringField(validators=[Length(min=2, max=20, message="Wrong Password!")])
    Password2 = wtforms.StringField(validators=[EqualTo("Password1")])

    # 验证邮箱验证码的 先不管
    # def validate_email(self, field):
    #     email = field.data
    #     user = UserModel.query.filter_by(email=email).filter()
    #     if user:
    #         raise wtforms.ValidationError(message="The email has been registered!")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Wrong Format!!!!")])
    Password1 = wtforms.StringField(validators=[Length(min=2, max=20, message="Wrong Password!!!!!")])


class PostForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="Wrong title format!")])
    content = wtforms.StringField(validators=[Length(min=3, message="Wrong content format!")])


class CommentForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="Wrong content format!!")])
    post_id = wtforms.IntegerField(validators=[InputRequired(message="Post-id is a must!")])
