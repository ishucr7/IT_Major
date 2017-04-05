from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db

mod_report = Blueprint('enrolment', __name__)

# Your controllers here
