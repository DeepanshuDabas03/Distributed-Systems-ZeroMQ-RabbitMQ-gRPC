from concurrent import futures
import time
import grpc
import shopping_platform_pb2
import shopping_platform_pb2_grpc

categories={
    0: "Electronics",
    1: "Fashion",
    2: "Others",
}
sellers = {}  # Dictionary to store seller registrations
items = {}  # Dictionary to store items listed on the market
items_ratings = {}  # Dictionary to store ratings for items
buyers = {}  # Dictionary to store buyer registrations
notifications=[]
notification_address =[]
buyers_wishlist = {}  # Dictionary to store buyer wishlists
class MarketServicer(shopping_platform_pb2_grpc.BuyerServiceServicer,shopping_platform_pb2_grpc.SellerServiceServicer):
    def __init__(self):
       pass

    def Notify_Subscribers(self,message,item_id):
        #check if the notification address is already in the list
        for item in buyers_wishlist:
            if item_id in buyers_wishlist[item]:
                notification_address.append(item)
                notifications.append(shopping_platform_pb2.Notification(message=message))
            

    def RegisterSeller(self, request, context):
        if request.address not in sellers:
            sellers[request.address] = request.uuid
            print(f"Seller join request from {request.address}, uuid = {request.uuid}")
            return shopping_platform_pb2.SellerRegistrationResponse(status=shopping_platform_pb2.SellerRegistrationResponse.Status.SUCCESS)
        else:
            print(f"Address {request.address} already registered.")
            return shopping_platform_pb2.SellerRegistrationResponse(status=shopping_platform_pb2.SellerRegistrationResponse.Status.FAIL)

    def SellItem(self, request, context):
        if(request.seller_address not in sellers):
            print(f"Seller {request.seller_address} not found.")
            return shopping_platform_pb2.SellItemResponse(status=shopping_platform_pb2.SellItemResponse.Status.FAIL)
        if(sellers[request.seller_address] != request.seller_uuid):
            print(f"UUID does not match for seller {request.seller_address}")
            return shopping_platform_pb2.SellItemResponse(status=shopping_platform_pb2.SellItemResponse.Status.FAIL)
        item_id = len(items) + 1  # Assign unique item id
        items[item_id] = request
        items_ratings[item_id] = []
        print(f"Sell Item request from {request.seller_address}")
        return shopping_platform_pb2.SellItemResponse(status=shopping_platform_pb2.SellItemResponse.Status.SUCCESS, item_id=str(item_id))

    def UpdateItem(self, request, context):
        if(request.seller_address not in sellers):
            print(f"Seller {request.seller_address} not found.")
            return shopping_platform_pb2.UpdateItemResponse(status=shopping_platform_pb2.UpdateItemResponse.Status.FAIL)
        if(sellers[request.seller_address] != request.seller_uuid):
            print(f"UUID does not match for seller {request.seller_address}")
            return shopping_platform_pb2.UpdateItemResponse(status=shopping_platform_pb2.UpdateItemResponse.Status.FAIL)
        if int(request.item_id) in items:
            items[int(request.item_id)].price = request.new_price
            items[int(request.item_id)].quantity = request.new_quantity
            print(f"Update Item {request.item_id} request from {request.seller_address}")
            try:
                message= f"\nThe Following Item has been updated:Item ID: {request.item_id}, Price: {request.new_price},Category: {categories[items[int(request.item_id)].category]}, \nDescription: {items[int(request.item_id)].description}, \nQuantity: {request.new_quantity},\nRating: {sum(items_ratings[int(request.item_id)]) / len(items_ratings[int(request.item_id)]) if len(items_ratings[int(request.item_id)]) > 0 else 5.00}, \nSeller: {items[int(request.item_id)].seller_address}"
                self.Notify_Subscribers(message=message,item_id=request.item_id)
            except Exception as e:
                print(e)
            return shopping_platform_pb2.UpdateItemResponse(status=shopping_platform_pb2.UpdateItemResponse.Status.SUCCESS)
        else:
            print(f"Item with ID {request.item_id} not found.")
            return shopping_platform_pb2.UpdateItemResponse(status=shopping_platform_pb2.UpdateItemResponse.Status.FAIL)

    def DeleteItem(self, request, context):
        if(request.seller_address not in sellers):
            print(f"Seller {request.seller_address} not found.")
            return shopping_platform_pb2.DeleteItemResponse(status=shopping_platform_pb2.DeleteItemResponse.Status.FAIL)
        if(sellers[request.seller_address] != request.seller_uuid):
            print(f"UUID does not match for seller {request.seller_address}")
            return shopping_platform_pb2.DeleteItemResponse(status=shopping_platform_pb2.DeleteItemResponse.Status.FAIL)
        if int(request.item_id) in items:
            del items[int(request.item_id)]
            print(f"Delete Item {request.item_id} request from {request.seller_address}")
            return shopping_platform_pb2.DeleteItemResponse(status=shopping_platform_pb2.DeleteItemResponse.Status.SUCCESS)
        else:
            print(f"Item with ID {request.item_id} not found.")
            return shopping_platform_pb2.DeleteItemResponse(status=shopping_platform_pb2.DeleteItemResponse.Status.FAIL)

    def DisplaySellerItems(self, request, context):
        if(request.seller_address not in sellers):
            print(f"Seller {request.seller_address} not found.")
            return shopping_platform_pb2.DisplaySellerItemsResponse(items=[])
        items_list = []
        for item_id, item in items.items():
            if item.seller_address == request.seller_address and sellers[request.seller_address] == request.seller_uuid:
            # Create an ItemDetails object for each item
                item_details = shopping_platform_pb2.DisplaySellerItemsResponse.ItemDetails(
                    item_id=str(item_id),
                    price=item.price,
                    product_name=item.product_name,
                    category=item.category,
                    description=item.description,
                    quantity_remaining=item.quantity,
                    rating=sum(items_ratings[item_id]) / len(items_ratings[item_id]) if len(items_ratings[item_id]) > 0 else 5.00,
                    seller=item.seller_address  # Assuming seller_address is the seller's address
                )
                items_list.append(item_details)
        if(sellers[request.seller_address] != request.seller_uuid):
            print(f"UUID does not match for seller {request.seller_address}")
            return shopping_platform_pb2.DisplaySellerItemsResponse(items=[])
        else:
            print(f"Display Items request from {request.seller_address}")
            # Create and return the DisplaySellerItemsResponse
            return shopping_platform_pb2.DisplaySellerItemsResponse(items=items_list)
        
    # BuyerServiceServicer methods
    def SearchItem(self, request, context):
        # Implement searching item logic
        items_list = []
        for item_id, item in items.items():
            if request.item_name!="" and item.product_name.lower() != request.item_name.lower() :
                continue
            if request.category != shopping_platform_pb2.SearchItemRequest.Category.ANY and item.category != request.category:
                continue
            item_details = shopping_platform_pb2.SearchItemResponse.ItemDetails(
                item_id=str(item_id),
                price=item.price,
                product_name=item.product_name,
                category=item.category,
                description=item.description,
                quantity_remaining=item.quantity,
                rating=sum(items_ratings[item_id]) / len(items_ratings[item_id]) if len(items_ratings[item_id]) > 0 else 5.00,
                seller=item.seller_address
            )
            items_list.append(item_details)
        return shopping_platform_pb2.SearchItemResponse(items=items_list)

    def BuyItem(self, request, context):
        # Implement buying item logic
        if int(request.item_id) in items:
            item = items[int(request.item_id)]
            if item.quantity >= request.quantity:
                print(f"Buy request {request.quantity} of item {request.item_id} from {request.buyer_address}")
                notification_address.append(item.seller_address)
            
                #add notification functionality
                notifications.append(shopping_platform_pb2.Notification(message=f"\nThe Following Item has been bought:\nItem ID: {request.item_id}, Price: {item.price}\n, Category: {categories[item.category]}\n, Description: {item.description}\n, Quantity: {request.quantity}\n,Rating: {sum(items_ratings[int(request.item_id)]) / len(items_ratings[int(request.item_id)]) if len(items_ratings[int(request.item_id)]) > 0 else 5.00}\n, Seller: {item.seller_address}"))
                item.quantity -= request.quantity
                return shopping_platform_pb2.BuyItemResponse(status=shopping_platform_pb2.BuyItemResponse.Status.SUCCESS)
            else:
                return shopping_platform_pb2.BuyItemResponse(status=shopping_platform_pb2.BuyItemResponse.Status.FAIL)
        else:
            return shopping_platform_pb2.BuyItemResponse(status=shopping_platform_pb2.BuyItemResponse.Status.FAIL)

    def AddToWishlist(self, request, context):
        # Implement adding to wishlist logic
        if int(request.item_id) in items:
            if request.buyer_address not in buyers_wishlist:
                buyers_wishlist[request.buyer_address] = set()
            buyers_wishlist[request.buyer_address].add(request.item_id)
            return shopping_platform_pb2.AddToWishlistResponse(status=shopping_platform_pb2.AddToWishlistResponse.Status.SUCCESS)
        else:
            return shopping_platform_pb2.AddToWishlistResponse(status=shopping_platform_pb2.AddToWishlistResponse.Status.FAIL)

    def RateItem(self, request, context):
        # Implement rating item logic
        if request.rating < 0 or request.rating > 5:
            return shopping_platform_pb2.RateItemResponse(status=shopping_platform_pb2.RateItemResponse.Status.FAIL)
        item_id = int(request.item_id)
        if item_id in items_ratings and request.buyer_address not in items_ratings[item_id]:
            items_ratings[item_id].append(request.rating)
            print(f"{request.buyer_address} rated item {item_id} with {request.rating} stars")
            return shopping_platform_pb2.RateItemResponse(status=shopping_platform_pb2.RateItemResponse.Status.SUCCESS)
        else:
            return shopping_platform_pb2.RateItemResponse(status=shopping_platform_pb2.RateItemResponse.Status.FAIL)

    def NotifyClient(self, request, context):
        if len(notifications) == 0:
            return shopping_platform_pb2.NotifyClientResponse(status=shopping_platform_pb2.NotifyClientResponse.Status.FAIL)
        else:
            if notification_address[0] == request.address:
                notification_address.pop(0)
                if len(notifications) > 0:
                    return shopping_platform_pb2.NotifyClientResponse(
                status=shopping_platform_pb2.NotifyClientResponse.Status.SUCCESS,
                notification=notifications.pop(0)
            )
            else:
                return shopping_platform_pb2.NotifyClientResponse(status=shopping_platform_pb2.NotifyClientResponse.Status.FAIL)

    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_platform_pb2_grpc.add_BuyerServiceServicer_to_server(MarketServicer(), server)
    shopping_platform_pb2_grpc.add_SellerServiceServicer_to_server(MarketServicer(), server)
    Server_Address = input("Enter the server address: ")
    server.add_insecure_port(Server_Address)
    server.start()
    print("Market server started on " + Server_Address)
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
