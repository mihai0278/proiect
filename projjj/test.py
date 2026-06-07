import socket
import sqlite3
import ssl

try :
    db = sqlite3.connect('/opt/server-py/comunicatii.db')
    cursor = db.cursor()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
    certfile = "/etc/letsencrypt/live/proiectt.sbs/fullchain.pem", 
    keyfile = "/etc/letsencrypt/live/proiectt.sbs/privkey.pem"
)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0',5005))
    server.listen(1)
    print("server pornit,asteapta conectiuni...")
except sqlite3.Error as e :
    print(f"❌ Database error: {e}")
except Exception as e :
    print(f"❌ Server error: {e}")



while True :
    try :
        fir_neprotejat, adresa = server.accept()
        print(f"conexiune de la {adresa}")
        with context.wrap_socket(fir_neprotejat, server_side=True) as fir_protejat:
            mesaj_total = ""
            while True:
                date_raw = fir_protejat.recv(4)
                if not date_raw:
                     break
                mesaj_total += date_raw.decode()
                

                if not mesaj_total:
                    print("❌ No data received")
                    continue

            cursor.execute("""
                    INSERT INTO loguri (expeditor, mesaj, timestamp) 
                    VALUES (?, ?, datetime('now', 'localtime'))
                """, (adresa[0], mesaj_total))
            db.commit()
            print(f"comanda primita: {mesaj_total}")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Client error: {e}")
    finally:
        if fir_neprotejat:
            fir_neprotejat.close()
