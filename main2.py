from data import db_session
from data.jobs import Jobs

db_session.global_init("db/mars_explorer.sqlite")

job = Jobs()
job.team_leader = "1"
job.job = "deployment of residential modules"
job.work_size = "15"
job.collaborators = "2, 3"
job.speciality = "research engineer"
job.is_finished = False

session = db_session.create_session()
session.add(job)
session.commit()
