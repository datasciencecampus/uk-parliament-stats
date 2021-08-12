import sys
import requests
import os


savepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'outputs', 'data'))
url = 'https://storage.googleapis.com/harvard-dataverse/Corp_HouseOfCommons_V2.csv'

def download_rds_file():
    path = os.path.join(os.path.join(savepath,f'Corp_HouseOfCommons_V2.csv'))

    check_file = os.path.isfile(path)
    if not check_file:
        with open(path, "wb") as f:
            print(f"Downloading to {path}")
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
    else:
        print(f'File exists already as {path}.')