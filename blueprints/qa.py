from flask import Blueprint, request, render_template, g, redirect, url_for, flash,session
from forms import PostForm, CommentForm
from models import PostModel, CommentModel
from exts import db
from decorators import login_required


bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    return render_template("index.html", posts=posts)

@bp.route("qa/post", methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'GET':
        return render_template("add_post.html")
    else:
        form = PostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            post = PostModel(title=title, content=content, author=g.user)
            db.session.add(post)
            db.session.commit()
           # todo；跳转到详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.add_post"))


@bp.route("/qa/detail/<ep_id>")
def qa_detail(ep_id):
    post = PostModel.query.get(ep_id)
    return render_template("experience_detail.html", post=post, ep_id=ep_id)


@bp.route("/comment/publish", methods=["post"])
@login_required
def publish_comment():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        comment = CommentModel(content=content, post_id=post_id, author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", ep_id=post_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", ep_id=request.form.get("post_id")))


@bp.route("/search")
def search():
    q = request.args.get("q")
    if q is not None:
        posts = PostModel.query.filter(PostModel.title.contains(q)).all()
        return render_template("index.html", posts=posts)
    else:
        flash("Invalid search query.", "error")
        return redirect(url_for("qa.index"))


@bp.route("/delete_comment/<comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = CommentModel.query.get(comment_id)

    # 检查当前用户是否为评论的作者
    user_id = session.get('user_id')  # 从会话中获取用户ID
    if user_id and comment.author_id == user_id:
        db.session.delete(comment)
        db.session.commit()
        flash('评论删除成功！', 'success')
    else:
        flash('您没有权限删除此评论。', 'danger')
    return redirect(url_for("qa.qa_detail", ep_id=comment.post_id))
