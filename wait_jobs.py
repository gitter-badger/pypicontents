
import os
import time
from travispy import TravisPy

api = TravisPy.github_auth(os.getenv('GHTOKEN'))
repo = api.repo('LuisAlejandro/pypicontents')
build = api.build(os.getenv('TRAVIS_BUILD_ID'))

while [j for j in build.job_ids
       if str(api.job(j).state) != str('passed') and
       str(j) != str(os.getenv('TRAVIS_JOB_ID'))]:
    print("Waiting for jobs to finish ...")
    time.sleep(60)
