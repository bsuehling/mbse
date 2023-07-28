
import zlib
import base64
import string

import requests
import shutil

def img_request(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def simplify_messages_out(messages_out):
    ans = ""
    for m in messages_out:
        if ans != "":
            ans+= "\\n"
        ans+=f"<{m.operation}, {m.receiver}, {m.return_value}>"
    return ans

def io_automata_viz(automat, filename):
    #plant uml viz
    command = '@startuml\nhide empty description\n'
    command+=f"[*] -> {automat.states[0]}\n"
    for t in automat.transitions:
        line = f'{t.pre_state} -> {t.post_state} : {t.message_in} / {simplify_messages_out(t.messages_out)} return={t.return_value}\n'
        command += line
    command+='@enduml\n\n'
    
    plantuml_url = f"https://www.plantuml.com/plantuml/png/{plantuml_encode(command)}"
    img_request(plantuml_url, filename)
    return plantuml_url
    

# encoding decoding code from ryardley
# https://gist.github.com/ryardley/88001f6822975ece088d41768431f5d6

maketrans = bytes.maketrans

plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet   = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))
plantuml_to_b64 = maketrans(plantuml_alphabet.encode('utf-8'), base64_alphabet.encode('utf-8'))

def plantuml_encode(plantuml_text):
    """zlib compress the plantuml text and encode it for the plantuml server"""
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')

def plantuml_decode(plantuml_url):
    """decode plantuml encoded url back to plantuml text"""
    data = base64.b64decode(plantuml_url.translate(plantuml_to_b64).encode("utf-8"))
    dec = zlib.decompressobj() # without check the crc.
    header = b'x\x9c'
    return dec.decompress(header + data).decode("utf-8")
    
    