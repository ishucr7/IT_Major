from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db

mod_courses = Blueprint('courses', __name__)

@mod_courses.route('/courses', methods=['GET'])
def get_all_courses():
    pass
