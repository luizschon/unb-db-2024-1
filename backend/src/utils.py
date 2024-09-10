import base64

def encode_base64(input):
    return base64.b64encode(input).decode('utf-8')

def parse_formdata(decoded_multipart):
    data = {}
    for part in decoded_multipart.parts:
        content_disposition = part.headers.get(b'Content-Disposition').decode("utf-8")
        disposition_string = content_disposition.split('; ')
        disposition_data = {}

        for field in disposition_string[1:]:
            print(field)
            split = field.split('=', 1)
            key = split[0]
            value = split[1][1:-1]
            disposition_data[key] = value

        name = disposition_data.get('name')
        filename = disposition_data.get('filename')
        print(name)

        if filename:
            data[name] = part.content
        else:
            data[name] = part.text

    return data

def parse_tsrange(range):
    return {
        "start_time": range.lower.isoformat(),
        "end_time": range.upper.isoformat()
    }
