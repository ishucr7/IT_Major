from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db

mod_students = Blueprint('students', __name__)

@mod_students.route('/students', methods=['GET'])
def get_all_students():
    pass

