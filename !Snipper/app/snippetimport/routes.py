from app.snippetimport import snippetimport_bp
from flask import render_template, flash, redirect, url_for
from app.snippetimport.forms import SnippetImportForm
from flask_login import current_user, login_required
from app import db
from app.models import Snippet

@snippetimport_bp.route('/import', methods=['GET', 'POST'])
@login_required
def snippetimport():
    form = SnippetImportForm()

    # If form is submitted, add new data to db and commit the session
    if form.validate_on_submit():
        snippet = Snippet(snippet=form.snippet.data, source=form.source.data, author=form.author.data,source_type=form.source_type.data, user=current_user)
        db.session.add(snippet)
        db.session.commit()
        flash('Your snippet has been added successfully!', 'success')
        return redirect(url_for('snippetimport.snippetimport'))   

    # Else render the form for user to fill out
    return render_template('snippetimport.html', title='Snippet Import', form=form)
