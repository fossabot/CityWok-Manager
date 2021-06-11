# from citywok_ms import db
# from citywok_ms.models import Employee, File
# from flask import request


# class TestDelete:
#     def test_get(self, test_client, test_files):
#         response = test_client.get('/file/1/delete')
#         assert response.status_code == 405

#     def test_valid_post(self, test_client, test_files):
#         response = test_client.post('/file/1/delete',
#                                     follow_redirects=True)
#         assert response.status_code == 200
#         assert 'File has been move to trash bin' in response.data.decode(
#             'utf-8')
#         response = test_client.post('/file/1/delete',
#                                     follow_redirects=True)
#         assert response.status_code == 200
#         assert 'File has already been deleted' in response.data.decode(
#             'utf-8')

#     def test_invalid_post(self, test_client, test_files):
#         response = test_client.post('/file/101/delete',
#                                     follow_redirects=True)
#         assert response.status_code == 404


# class TestRestore:
#     def test_get(self, test_client, test_files):
#         response = test_client.get('/file/2/restore')
#         assert response.status_code == 405

#     def test_valid_post(self, test_client, test_files):
#         response = test_client.post('/file/2/restore',
#                                     follow_redirects=True)
#         assert response.status_code == 200
#         assert 'File has been restore' in response.data.decode(
#             'utf-8')
#         response = test_client.post('/file/2/restore',
#                                     follow_redirects=True)
#         assert response.status_code == 200
#         assert "File hasn&#39;t been deleted" in response.data.decode(
#             'utf-8')

#     def test_invalid_post(self, test_client, test_files):
#         response = test_client.post('/file/101/restore',
#                                     follow_redirects=True)
#         assert response.status_code == 404


# class TestUpdate:
#     def test_get(self, test_client, test_files):
#         response = test_client.get('/file/1/update')
#         assert response.status_code == 200
#         assert b'emp_1' in response.data
#         assert b'Update File' in response.data
#         assert b'action="/file/1/update"'

#     def test_post(self, test_client, test_files):
#         data = dict(file_name='changed',
#                     remark='remark')
#         response = test_client.post('/file/1/update',
#                                     data=data,
#                                     follow_redirects=True)
#         assert response.status_code == 200
#         assert request.url.endswith('/employee/1')
#         f = db.session.query(File).get(1)
#         assert f.file_name == 'changed'
#         assert f.remark == 'remark'
#         assert 'File has been update' in response.data.decode(
#             'utf-8')


# class TestDownload:
#     def test_get(self, test_client, test_files):
#         response = test_client.get('/file/1/download', follow_redirects=True)
#         assert response.status_code == 200
#         assert b'test_file_content' in response.data
