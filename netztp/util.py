from flask import make_response
import hashlib

def response_with_content_type(data, content_type):
    response = make_response(data)
    response.headers['Content-Type'] = content_type
    return response

def generate_checksum(obj):
    checksum = hashlib.sha1(obj.encode('utf-8')).hexdigest()
    size = len(obj)
    return {
        'sha1': checksum,
        'size': size
    }
