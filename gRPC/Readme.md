



# Online Shopping Platform

This project implements an Online Shopping Platform using gRPC, python and protocol buffer, allowing buyers and sellers to interact with a central Market . The platform facilitates various functionalities such as seller registration, item listing, item updates, purchases, wishlists, and ratings.



## Components



### Market (Central Platform):



- The Market serves as the central platform connecting sellers and buyers.

- It manages seller accounts, items for sale, transactions, reviews, and notifications.

- Buyers and sellers communicate with the Market, which is deployed at a known address (ip:port).



### Seller:



- Sellers register with the Market by providing their address (ip:port) and a unique UUID.

- They can add, update, delete, and display their items for sale by using gRPC calls. 

- Sellers receive notifications about their items and transactions by continuously trying to fetch notifications from market. 



### Buyer:



- Buyers interact with the Market to search for and purchase items.

- They can also wishlist items to receive notifications about updates.

- Buyers can rate items and all individual rating are stored anonymous and there combined average is calculated as final rating. By default  if a product is not rated, it will be rated 5 stat by default.



## Communication



All communication between components happens using protocol buffers (protos). Each functionality has its own proto-definitions.



## Server Implementation



The server side of the platform is implemented in Python using gRPC. Market serves as the gRPC server, handling requests from sellers and buyers. Each functionality is implemented as an RPC method in the servicer class of each client BuyerServiceServicer And SellerServiceServicer.



## Client Implementation



The client side of the platform is also implemented in Python using gRPC. Clients interact with the Market  by making RPC calls to perform various actions such as seller registration, item listing, purchases, etc.

For fetching notifications, a continuous thread is running in the background which checks with server whether there is an update for client( if product is in wishlist)

## Prerequisites



- Python 3.x

- gRPC Python library

- Protocol Buffer compiler (protoc)



## How to Run



1. Ensure you have Python and the required dependencies installed.

2. Generate protocol buffer files from the provided `.proto` definitions.

3. Start the server by running the provided Python script for the Market first.

4. Run the seller script to interact with the platform as a seller and register and add products. Buyer than can wishlist a product and also can make purchases.



## Contributors:

-	This project was developed by Deepanshu Dabas and Rudra Jyotirmay as part of Assignment 1.

