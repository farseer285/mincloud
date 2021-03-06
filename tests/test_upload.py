import io

from app import db
from app.models import User
from app.constants import responds
from tests.test_base import BaseTest
from tests.testhelper import login, add_new_user, upload_file, make_file_public


class TestUpload(BaseTest):
    def test_uploadsite(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        user.admin = False

        db.session().add(user)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertTrue('index_page_7890' in str(rv.data))
            rv = c.get('/upload', follow_redirects=True)
            self.assertTrue("upload_site_234889" in str(rv.data))

    def test_fileupload(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        user.admin = False

        db.session().add(user)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertTrue('index_page_7890' in str(rv.data))
            rv = c.get('/upload', follow_redirects=True)
            self.assertTrue("upload_site_234889" in str(rv.data))
            testfile_bytes = b"fdjasdfjksjkadf"
            testfile = (io.BytesIO(testfile_bytes), 'testing_134.txt')
            data = {'files[]': testfile}

            rv = c.post('/api/upload', data=data, follow_redirects=True,
                        content_type='multipart/form-data')

            ret = rv.json['files'][0]
            self.assertEqual('testing_134.txt', ret['name'])
            url = ret['url']

            getfile = c.get(url, follow_redirects=True)

            self.assertEqual(testfile_bytes, getfile.data)

    def test_api_makepublic(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        user.admin = False

        db.session().add(user)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertTrue('index_page_7890' in str(rv.data))
            rv = c.get('/upload', follow_redirects=True)
            self.assertTrue("upload_site_234889" in str(rv.data))
            testfile_bytes = b"fdjasdfjksjkadf"
            testfile = (io.BytesIO(testfile_bytes), 'testing_134.txt')
            data = {'files[]': testfile}

            rv = c.post('/api/upload', data=data, follow_redirects=True,
                        content_type='multipart/form-data')

            ret = rv.json['files'][0]
            self.assertEqual('testing_134.txt', ret['name'])
            url = ret['url']

            getfile = c.get(url, follow_redirects=True)

            self.assertEqual(testfile_bytes, getfile.data)

            uid = ret['uid']
            rv = make_file_public(c, uid)

            self.assertTrue(responds['PUBLIC_KEY_GENERATED'] in str(rv.json['response']))

            dlurl = rv.json['url']

            getfile = c.get(dlurl, follow_redirects=True)
            self.assertEqual(testfile_bytes, getfile.data)









