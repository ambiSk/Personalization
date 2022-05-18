import requests, base64, json, os, cv2, ntpath, time

class ImageAPI:
    def __init__(self, ):
        self.URL_POST = "http://10.20.6.17:5002/ds/internal/v1/selfie"
        self.URL_GET = "http://10.20.6.17:5002/ds/internal/v1/selfie/%s?uid=test&msisdn=test&type=data"
        
        self.URL_CONVERT_API = "http://10.20.6.17:5010/ds/internal/v1/convert_data"
        self.URL_RENDER_API = "http://10.20.1.194:3002/processimage/getHikemoji3dImage"
    
    def send_request(self, filename, bufferReader, gender):
        payload = dict(
            gender = gender,
            version = 'v6-99999999',
            uid = 'test',
            msisdn = 'test',
            app_name = 'rush',
            type = 'data',
            inference_type = '2D',
            lod = 'a'
            )
        files = [
            ('file' , (filename, bufferReader, 'image/png'))
            ]
        response = requests.post(self.URL_POST, files=files, data=payload, headers = {}, timeout = 5)
        
        return response.json()['id']
    
    def get_data(self, request_id):
        payload = {}

        response = requests.get(self.URL_GET % request_id, headers={}, data=payload, timeout = 5)
    #     print("Response", response.text)
        response = response.json()["data"]

        return response
    
    def get_3d_data(self, data_2d, gender):
    
        data_2d[gender.capitalize() + "FaceShape"]['color'] = data_2d['SkinColor']

        payload = json.dumps({"uid": "test_user", "data": data_2d, 
                              "gender": gender, "app_name": 'rush', 'type': '2d_to_3d'})
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.post(self.URL_CONVERT_API, headers=headers, data=payload)

        return response.json()
    
    def get_3d_render(self, data_3d, gender):
        data_3d = data_3d['data']
        data_3d['lod'] = 's'
        data_3d['models']['BaseBody'] = dict(name = 'BaseBody_BodyMesh_Basic_01_Main')

        payload = json.dumps({"data": data_3d, "gender": gender, "version": "v1", "createTorsoAvatar": True})

        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.post(self.URL_RENDER_API, headers=headers, data=payload)

        return response.json()


    def save_render_3d(self, render_3d, image_name):
        render_3d = render_3d['avatar']

        with open(os.path.join(image_name + ".png"), "wb") as fh:
            fh.write(base64.decodebytes(bytes(render_3d, 'utf-8')))

    def __call__(self, filename, bufferReader, gender):
        out = self.send_request(filename, bufferReader, gender)
        time.sleep(3)
        out = self.get_data(out)
        out = self.get_3d_data(out, gender)
        out = self.get_3d_render(out, gender)
        return out['avatar']
        
        
        