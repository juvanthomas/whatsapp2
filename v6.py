from flask import Flask, request
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import requests
import uuid
from flask import send_file

#  data of the url of views
dashboard_urls = {
    'promotion': "https://ask.beinex.com//api/3.9/sites/908f81e2-cb30-43a2-a7d0-461879aa9016/views/1829f8ea-00a7-490f-b0cd-97fd55a6e710/image",
    'ticket_sales': "https://ask.beinex.com//api/3.9/sites/908f81e2-cb30-43a2-a7d0-461879aa9016/views/250d968b-51ca-461d-a1a7-662e8f0aefb1/image",
    'ticket_group': "https://ask.beinex.com//api/3.9/sites/908f81e2-cb30-43a2-a7d0-461879aa9016/views/8d28d450-e92a-4894-8707-2f57a73d3038/image"
}

maping = {"1": "promotion",
          "2": "ticket_sales",
          "3": "ticket_group"
          }
maping_for_display = {"promotion": "Promotion Performance",
                      "ticket_sales": "Ticket Sales Overview",
                      "ticket_group": "Website Sales"}

# ~ logic of the program starts here
def create_app():


    app = Flask(__name__)


    @app.route("/")
    def hello():
        return "#########"

    @app.route("/get-image/<image_name>")
    def get_image(image_name):
        print(image_name)
        path ='/home/juvanthomas/PycharmProjects/whatsap_tableau/documents/'
        #path ='/home/ubuntu/sreejith_whatsaap/documents/'
        file =path+image_name
        return send_file(path_or_file=file, as_attachment=False)


    @app.route("/sms", methods=['POST'])
    def sms_reply():
        """Respond to incoming calls with a simple text message."""
        # Fetch the message
        msg = request.form.get('Body')  # whatsap
        # mobile = request.form.get('From')
        query = str(msg)
        try:
            dashboard_name = maping[query]
            keyword = dashboard_urls[maping[query]]
            print(maping[query])
            print('keyword = ', keyword)

            if type(keyword) == str:
                token = log_in()
                HEADERS = {'X-Tableau-Auth': token}
                r = requests.get(url=keyword, headers=HEADERS, verify=False)
                object_name = str(uuid.uuid4())
                folder = "documents/"
                file_to_save = folder + object_name + '.png'
                with open(file_to_save, 'wb') as f:
                    f.write(r.content)
                    print("Succesfully generated and saved the datasource in Local")
                    print("http://0.0.0.0/:8081/get-image/" + object_name+'.png')
                    #print("http://3.6.141.16/:8080/get-image/" + object_name+'.png')

                local_url = "http://0.0.0.0:8081/get-image/" + object_name+'.png'
                #local_url = "http://3.6.141.16:8080/get-image/" + object_name+'.png'

                print(local_url)

                response = MessagingResponse()
                response.message("Your dashboard is loading ")

                # print(url)

                # Create 1st attachment

                message1 = Message()
                message1.body(maping_for_display[dashboard_name])
                message1.media(local_url)
                response.append(message1)

        except Exception as e:
            print(e)
            response = MessagingResponse()
            response.message(
                "\nBelow are the dashboards available. \nReply with the corresponding number to view it. \n\n 1. Promotion Performance  \n 2. Ticket Sales Overview  \n 3. Website Sales")

        return str(response)
    return app



def log_in():
    URL = "https://ask.beinex.com/api/3.6/auth/signin"

    xml = """<tsRequest>
            <credentials name="juvan" password="Juvan@123">
            <site contentUrl="Expo" />
            </credentials>
            </tsRequest>"""

    head = {"Accept": "application/json"}

    r = requests.post(url=URL, data=xml, headers=head, verify=False)
    jsonfile = r.json()
    token = jsonfile["credentials"]["token"]
    return token


