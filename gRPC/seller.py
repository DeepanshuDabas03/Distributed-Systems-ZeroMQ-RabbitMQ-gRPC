import grpc
import uuid
import threading
import shopping_platform_pb2
import shopping_platform_pb2_grpc

categories={
    0: "Electronics",
    1: "Fashion",
    2: "Others",
}


class SellerClient():
    def __init__(self,server_address="localhost:50051",Address="localhost:12345"):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = shopping_platform_pb2_grpc.SellerServiceStub(self.channel)
        self.Address=Address
        self.notification_thread = threading.Thread(target=self.receive_notifications, daemon=True)
        self.notification_thread.start()


    def register_seller(self, address, uuid):
        request = shopping_platform_pb2.SellerRegistrationRequest(
            address=address,
            uuid=uuid
        )
        response = self.stub.RegisterSeller(request)
        if response.status == shopping_platform_pb2.SellerRegistrationResponse.Status.SUCCESS:
            print("Seller registered successfully.")
        else:
            print("Failed to register seller.")


    def sell_item(self, product_name, Category, quantity, description, seller_address, price, seller_uuid):
        request = shopping_platform_pb2.SellItemRequest(
            product_name=product_name,
            category=Category,
            quantity=quantity,
            description=description,
            seller_address=seller_address,
            price=price,
            seller_uuid=seller_uuid
        )
        
        response = self.stub.SellItem(request)
        if response.status == shopping_platform_pb2.SellItemResponse.Status.SUCCESS:
            print("Item listed successfully. Item ID:", response.item_id)
        else:
            print("Failed to list item.")



    def update_item(self, item_id, new_price, new_quantity, seller_address, seller_uuid):
        request = shopping_platform_pb2.UpdateItemRequest(
            item_id=item_id,
            new_price=new_price,
            new_quantity=new_quantity,
            seller_address=seller_address,
            seller_uuid=seller_uuid
        )
        response = self.stub.UpdateItem(request)
        if response.status == shopping_platform_pb2.UpdateItemResponse.Status.SUCCESS:
            print("Item updated successfully.")
        else:
            print("Failed to update item.")



    def delete_item(self, item_id, seller_address, seller_uuid):
        request = shopping_platform_pb2.DeleteItemRequest(
            item_id=item_id,
            seller_address=seller_address,
            seller_uuid=seller_uuid
        )
        response = self.stub.DeleteItem(request)
        if response.status == shopping_platform_pb2.DeleteItemResponse.Status.SUCCESS:
            print("Item deleted successfully.")
        else:
            print("Failed to delete item.")



    def display_seller_items(self, seller_address, seller_uuid):
        request = shopping_platform_pb2.DisplaySellerItemsRequest(
            seller_address=seller_address,
            seller_uuid=seller_uuid
        )
        response = self.stub.DisplaySellerItems(request)
        if(len(response.items)==0):
            print("No items found")
            return
        print("Seller Items:\n-----------------")

        for item in response.items:
            print(f' Item ID: {item.item_id},Price: {item.price}, Name: {item.product_name}, Category: {categories[item.category]}\n Description: {item.description}\n Quantity Remaining: {item.quantity_remaining}\n Seller: {item.seller}\n Rating: {item.rating} / 5')
            print("-----------------")



    def receive_notifications(self):
        try:
            while(True):
                request = shopping_platform_pb2.NotifyClientRequest(address=self.Address)    
                response= self.stub.NotifyClient(request)
                if (response is None):
                    return
                if(response.status != shopping_platform_pb2.NotifyClientResponse.Status.FAIL):
                    print("Notification: ",response)
        except KeyboardInterrupt:
            pass



if __name__ == '__main__':
    Server_Address=input("Enter the server address: ")
    Address=input("Enter the address of the seller: ")
    seller_client = SellerClient(server_address=Server_Address,Address=Address)
    uud=str(uuid.uuid1())
    print(f"Welcome to the Shopping Platform! Seller with address {Address} and UUID {uud}")
    try:
        while(True):
            print("Please choose\n1. Register Seller\n2. Sell Item\n3. Update Item\n4. Delete Item\n5. Display Seller Items\n6. Exit")
            choice=int(input("Enter your choice: "))
            if(choice==1):
                seller_client.register_seller(address=Address, uuid=uud)
            elif(choice==2):
                product_name=input("Enter the product name: ")
                print("Categories:\n0. Electronics\n1. Fashion\n2. Others")
                category=int(input("Enter the category: "))
                quantity=int(input("Enter the quantity: "))
                description=input("Enter the description: ")
                price=input("Enter the price: ")
                seller_client.sell_item(product_name=product_name, Category=category, quantity=quantity, description=description, seller_address=Address, price=price, seller_uuid=uud)
            elif(choice==3):
                item_id=input("Enter the item id: ")
                new_price=input("Enter the new price: ")
                new_quantity=int(input("Enter the new quantity: "))
                seller_client.update_item(item_id=item_id, new_price=new_price, new_quantity=new_quantity, seller_address=Address, seller_uuid=uud)
            elif(choice==4):
                item_id=input("Enter the item id: ")
                seller_client.delete_item(item_id=item_id, seller_address=Address, seller_uuid=uud)
            elif(choice==5):
                seller_client.display_seller_items(seller_address=Address, seller_uuid=uud)
            elif(choice==6):
                break
            else:
                print("Invalid choice")
    except KeyboardInterrupt:
        print("Exiting Application...")

  