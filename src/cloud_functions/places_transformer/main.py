########## global imports ##########


########## global vars ##########


########## classes & functions ##########
def parse_http_request(request: object) -> dict:
    try:
        request_args = request.args
        request_dict = request_args if type(request_args) is dict else dict(request_args)
        return request_dict
    except:
        return dict()

def process(request: object) -> tuple:
    try:
        # insert code here        
        print("### Running Cloud Function ###")        
        request_json = parse_http_request(request)
        print(f"### request_json={str(request_json)}")

        return ("OK", 200)
    except Exception as e:
        return (e, 500)

########## complete ##########