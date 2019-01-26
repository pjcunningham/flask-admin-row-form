# coding: utf-8

__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2019, Paul Cunningham'

from flask import redirect, flash, url_for
from flask_admin import expose
from flask_admin.contrib import sqla
from flask_admin.helpers import get_form_data
from flask_admin.babel import gettext
from markupsafe import Markup


class StudentView(sqla.ModelView):

    page_size = 5

    column_list = ('id', 'cost', 'Pay Now')
    column_editable_list = ['cost']

    # override the column labels
    column_labels = {
        'id': 'Student ID',
        'cost': 'Total Bill',
    }

    def _format_pay_now(view, context, model, name):

        if model.is_paid:
            return 'Paid'

        # render a form with a submit button for student, include a hidden field for the student id
        # note how checkout_view method is exposed as a route below
        checkout_url = url_for('.checkout_view')

        _html = '''
            <form action="{checkout_url}" method="POST">
                <input id="student_id" name="student_id"  type="hidden" value="{student_id}">
                <button type='submit'>Checkout</button>
            </form
        '''.format(checkout_url=checkout_url, student_id=model.id)

        return Markup(_html)

    column_formatters = {
        'Pay Now': _format_pay_now
    }

    @expose('checkout', methods=['POST'])
    def checkout_view(self):

        return_url = self.get_url('.index_view')

        form = get_form_data()

        if not form:
            flash(gettext('Could not get form from request.'), 'error')
            return redirect(return_url)

        # Form is an ImmutableMultiDict
        student_id = form['student_id']

        # Get the model from the database
        model = self.get_one(student_id)

        if model is None:
            flash(gettext('Student not not found.'), 'error')
            return redirect(return_url)

        # process the model
        model.is_paid = True

        try:
            self.session.commit()
            flash(gettext('Student, ID: {student_id}, set as paid'.format(student_id=student_id)))
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext('Failed to set student, ID: {student_id}, as paid'.format(student_id=student_id), error=str(ex)), 'error')

        return redirect(return_url)
