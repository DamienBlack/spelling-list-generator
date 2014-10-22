import os
if not 'SETTINGS' in os.environ:
    os.environ['SETTINGS'] = 'devel.cfg'

from spelling import app
app.run(host='0.0.0.0', port=8000)
