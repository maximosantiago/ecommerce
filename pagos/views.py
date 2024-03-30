from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from productos.models import Productos
from django.views.decorators.csrf import csrf_exempt
# SDK de Mercado Pago
import mercadopago
import requests
import json

def pagos(request, producto_id):
    #Traigo el producto
    
    producto = Productos.objects.get(id=producto_id)

    # Agrega credenciales. La SDK de mercadopago lo unico que hacer es hacer la peticion get a su api, porque si lo haces
    # por navegador, no te dejara.
    sdk = mercadopago.MP("APP_USR-5147934585933763-012723-f34438a8f2ef47bbebf5d4c88ea0650f-1656012877")

    # Crea un ítem en la preferencia
    preference_data = {
        "back_urls" :{
            "success": "http://127.0.0.1:8000/pagos/mp/exitoso"
        },
        "items": [
            {
                "id": str(producto.id),
                "title": producto.titulo,
                "description": "Descripcion: {}".format(producto.contenido),
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": float(producto.precio)
            }
        ],
        "notification_url":"https://c8e5-186-141-228-6.ngrok-free.app/pagos/mp/notificacion"
    }

    preference_response = sdk.create_preference(preference_data)
    preference = preference_response["response"]

    init_point_url = preference.get("init_point", "")
    return redirect(init_point_url)

def exito(request):

    return render(request, "pago_exitoso.html")


# En este ejemplo, la vista mercadopago_notification es decorada con @csrf_exempt para evitar problemas relacionados 
#con la protección contra CSRF. Además, se parsea el cuerpo de la solicitud JSON para obtener los datos de la notificación.
@csrf_exempt
def mercadopago_notification(request):
    if request.method == 'POST':
        
        # Procesar la notificación recibida
        data = json.loads(request.body.decode('utf-8')) #Con esto, se trae la peticion y se transcribe
        # Responder a Mercado Pago (si es necesario)
        # ...
        # Imprimir notificación en la consola del servidor
        print("Notificación recibida:", data)

        #¿Como acceder a la merchant order?


    
        headers = {
            'Authorization': 'Bearer APP_USR-5147934585933763-012723-f34438a8f2ef47bbebf5d4c88ea0650f-1656012877',
            'Content-Type': 'application/json',
        }
        try:

            if data["topic"] == "merchant_order":
                api_url = data.get("resource")

                if api_url is not None:

                    api = requests.get(api_url, headers = headers)

                    if api.status_code == 200:
                        response = api.json()
                        print(response)

                        #Explicacion de lo que devuelve merchant_order 

                        """
                            id: es igual al id de la order
                            Status: puede ser closed si se concreto la operacion
                            preference_id: es el id de la preferencia creada en la view de pagos
                            payments: es un array donde nos indica las caracteristica de los pagos realizados por cad producto
                            shipments: es por si se puso costo al envio
                            refunded_amount: es por si le haces una devolucion
                            items: es un array donde estan los objetos, cada objeto contiene caracteristicas del producto


                            ----------------------------Comprobacion del pago----------------------------------------

                            Para saber si el pago fue exitoso


                        """

                    else:
                        print("No se pudo conectar a la API")
                else:
                    print("N")
            elif data["topic"] == "payment":
                payment_url = data.get("resource")

                if payment_url is not None:

                    payment = requests.get(payment_url, headers=headers)

                    if payment.status_code == 200:

                        data_payment = payment.json()

                        print(data["topic"], "Getting payment", data_payment)

                        merchant_order_url = requests.get("https://api.mercadolibre.com/merchant_orders/{}".format(data_payment["order_id"]))

                        if merchant_order_url.status_code == 200:

                            merchant_order = merchant_order_url.json()

                            print("Getting merchant order:", merchant_order)

        except:
            print("No hay notificaciones")




    return HttpResponse(status=200)