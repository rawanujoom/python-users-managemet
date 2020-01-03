from flask import Flask, Response, request, send_from_directory
from flask_restplus import Api, Resource
import json
from handlers.resume_handler import ResumeHandler

app = Flask(__name__)
api = Api(app=app)
ns_conf = api.namespace('resume', description='resume operations')

resumeHandler = ResumeHandler()


@ns_conf.route("/")
class todo(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    def post(self):
        data = request.form.to_dict(flat=True)
        file = request.files["file"]

        output, status_code = resumeHandler.post_details(data, file)
        return Response(response=output, status=status_code)

    def get(self):
        admin = resumeHandler.check_admin(request.headers)
        if admin:
            data, status_code = resumeHandler.get_details()
            return Response(response=json.dumps(data), status=status_code)
        else:
            return Response(response="Not Authorized", status=403)


@ns_conf.route("/download/<string:id>")
class getResume(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    def get(self, id):
        admin = resumeHandler.check_admin(request.headers)
        if admin:
            uploads, filename = resumeHandler.get_applicant_resume(id)
            if uploads and filename:
                return send_from_directory(directory=uploads, filename=filename, as_attachment=True)
            return Response(response="No Such File", status=400)
        else:
            return Response(response="Not Authorized", status=403)


if __name__ == "__main__":
    app.run(debug=True)
