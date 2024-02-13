import grpc
import shopping_platform_pb2
import shopping_platform_pb2_grpc
import threading

class BuyerClient:
    def __init__(self, server_address="localhost:50051",address="localhost:52345"):
        self.address = address
        self.channel = grpc.insecure_channel(server_address)
        self.stub = shopping_platform_pb2_grpc.BuyerServiceStub(self.channel)
        self.notification_thread = threading.Thread(target=self.receive_notifications, daemon=True)
        self.notification_thread.start()


    def search_item(self, item_name="", category=shopping_platform_pb2.SearchItemRequest.ANY):
        request = shopping_platform_pb2.SearchItemRequest(item_name=item_name, category=category)
        response = self.stub.SearchItem(request)
        print("Search Results:")
        for item in response.items:
            print(item)

    def buy_item(self, item_id, quantity, buyer_address):
        request = shopping_platform_pb2.BuyItemRequest(item_id=item_id, quantity=quantity, buyer_address=buyer_address)
        response = self.stub.BuyItem(request)
        if response.status == shopping_platform_pb2.BuyItemResponse.Status.SUCCESS:
            print("Purchase successful.")
        else:
            print("Purchase failed.")

    def add_to_wishlist(self, item_id, buyer_address):
        request = shopping_platform_pb2.AddToWishlistRequest(item_id=item_id, buyer_address=buyer_address)
        response = self.stub.AddToWishlist(request)
        if response.status == shopping_platform_pb2.AddToWishlistResponse.Status.SUCCESS:
            print("Added to wishlist.")
        else:
            print("Failed to add to wishlist.")

    def rate_item(self, item_id, buyer_address, rating):
        request = shopping_platform_pb2.RateItemRequest(item_id=item_id, buyer_address=buyer_address, rating=rating)
        response = self.stub.RateItem(request)
        if response.status == shopping_platform_pb2.RateItemResponse.Status.SUCCESS:
            print("Rating submitted.")
        else:
            print("Failed to submit rating.")
    def receive_notifications(self):
        try:
            while(True):
                response= self.stub.NotifyClient(shopping_platform_pb2.NotifyClientRequest(address=self.address))
                if (response is None):
                    continue
                if(response.status != shopping_platform_pb2.NotifyClientResponse.Status.FAIL):
                    print("Notification: ",response.notification)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    Server_address = input("Enter the server address: ")
    buyer_address = input("Enter your buyer address: ")
    buyer_client = BuyerClient(Server_address, buyer_address)
    print(f"Welcome to the Shopping Platform! Buyer with address {buyer_address}")
    try:
        while(True):
            print("Please choose\n1. Search Item \n2. Buy Item \n3. Add to Wishlist \n4. Rate Item \n5. Exit")
            choice = int(input("Enter your choice: "))
            if(choice == 1):
                buyer_client.search_item()
            elif(choice == 2):
                item_id = input("Enter the item ID: ")
                quantity = int(input("Enter the quantity: "))
                buyer_client.buy_item(item_id, quantity, buyer_address)
            elif(choice == 3):
                item_id = input("Enter the item ID: ")
                buyer_client.add_to_wishlist(item_id, buyer_address)
            elif(choice == 4):
                item_id = input("Enter the item ID: ")
                rating = int(input("Enter the rating: "))
                buyer_client.rate_item(item_id, buyer_address, rating)
            elif(choice == 5):
                break
    except KeyboardInterrupt:
        print("Exiting Application...")
