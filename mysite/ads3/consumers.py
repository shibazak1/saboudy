
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Order, DriverOrder
from geopy.distance import geodesic
from django.utils.decorators import method_decorator

import json


class DriverTrackingConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        #websocket divide the connect to scop and envent scop is a dict like request that store
        # info about the connect  event is the action from client side 
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self room_group_name = f'order_{self.order_id}'# create and group name

        # add chennal (consumer instance ) to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        #accept the connection prefromed form the client 
        await self.accept()


    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)


    async def recieve(self,text_data):
        data = json.loads(text_data)
        order_id = data['order_id']
        lat = data['latitude']
        lng = data['longitude']

        status =  await self.process_order_status(order_id,lat,lng)
        

        # this will send the new up comming location to the group 
        await channel_layer.group_send(self.room_group_name,
                                       {'type':'location update',
                                        'status':status,
                                        'latitude':lat,
                                        'longitude':lng})

        

    async def update_location(self,event):

        # after recieveing the location to the group this will send to all client in the group
        await self.send(text_data = json.dumps({

            'latitude':event['latitude'],
            'longitude':event['longitdue'],
            'status':event['status']

        }))

        





        @database_sync_to_async
        def get_order(self,order_id):
            return get_object_or_404(Order,id=order_id)
        
        @database_sync_to_async
        def change_status(self,obj,status):
            obj.status=status
            obj.save()


        @database_sync_to_async
        def create_driver_order(self,order,driver):
            return DriverOrder.objects.create(order=order,driver=driver)

        
        @database_sync_to_async
        def process_order_status(order_id,lat,lng):

            if not order:
                order =  await self.get_order(order_id)

            customer_location = (order.latitude,order.longitude)
            driver_location = (lat,lng)

            distance = distance = geodesic(driver_location, customer_location).km

            if order.status = "PE":
                await self.change_status(order,"PR")
                driver_order = await self.create_driver_order(order,scope['user'])
            if distance<0.1:
                await self.change_status(order,"DE")
                await self.change_status(driver_order,"Delivered")

            return order.status

            
                
            
