import json
import socket
from encrypt_decrypt import CustomEncryption, CustomDecryption

# Create instances of encryption and decryption classes
custom_encryption = CustomEncryption()
custom_decryption = CustomDecryption()


# Function to retrieve encryption key from the user
def getting_key():
    user_key = input("Enter your encryption key for the whole process:")
    return user_key


# Function to send requests to the server
def send_request(request, user_key):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9192))
        client.settimeout(10)

        # Encrypt the request before sending
        encrypted_request = custom_encryption.perform_encryption(request, user_key)
        client.send(encrypted_request.encode())

        # Receive and decrypt the response
        encrypted_response = client.recv(4096).decode()
        decrypted_response = custom_decryption.perform_decryption(encrypted_response, user_key)
        return decrypted_response

    except socket.error as e:
        print(f"Socket error: {e}")
        return None
    except Exception as ex:
        print(f"Error: {ex}")
        return None
    finally:
        client.close()


# Regristration
def register_user(user_Key):
    print("User Registration:")
    username = input("Enter username: ")
    password = input("Enter password: ")
    contact_details = input("Enter contact details: ")
    return send_request(f"REGISTER:{username}:{password}:{contact_details}", user_Key)


# Create Auction for Login
def login(username, password, user_Key):
    return send_request(f"LOGIN:{username}:{password}", user_Key)


# Auctions Creations
def create_auction(user_Key):
    response = login(username, password, user_Key)
    print("****************:::Auction Creation:::********************")
    if "Login successful" in response:
        auction_id = input("Enter auction ID: ")
        title = input("Enter auction title: ")
        description = input("Enter auction description: ")
        end_time = input("Enter auction end time (e.g. 2024-01-01 12Hour 00Minutes): ")

        # Format the request properly
        request = f"CREATE_AUCTION:{auction_id}:{title}:{description}:{end_time}:{username}:{password}"
        return send_request(request, user_Key)
    else:
        print("Login failed. Unable to create an auction.")
        return


def display_all_users(user_Key):
    print("Display All Users")
    request = "DISPLAY_ALL_DATA"
    response = send_request(request, user_Key)

    if response:
        try:
            response_dict = json.loads(response)
            if response_dict:
                if 'users' in response_dict:
                    users = response_dict['users']
                    print("All Users:\n")
                    for user in users:
                        print(f"Username: {user['username']}")
                        print(f"Contact Details: {user['contact_details']}")
                        print("------------------------")
                else:
                    print("No user information available.")
            else:
                print("Received an empty response.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("No user information available.")


def place_bid(user_Key):
    print("@@@@@@@@@ Place Bid @@@@@@@@@@")
    auction_id = input("Enter auction ID to place a bid: ")
    username = input("Enter your username: ")
    bid_amount = input("Enter bid amount:$ ")

    # Construct the request to place a bid
    request = f"PLACE_BID:{auction_id}:{username}:{bid_amount}"
    response = send_request(request, user_Key)
    return response


def display_auction_status(user_Key):
    print("########### Display Auction Status #############")
    auction_id = input("Enter auction ID to display status: ")

    # Construct the request to display auction status
    request = f"DISPLAY_AUCTION_STATUS:{auction_id}"
    response = send_request(request, user_Key)
    return response


def modify_auction(user_Key):
    print("Modify Auction:")
    auction_id = input("Enter auction ID to modify: ")
    new_details = input("Enter new details for the auction: ")

    request = f"MODIFY_AUCTION:{auction_id}:{new_details}"
    response = send_request(request, user_Key)
    print("Modification :", response)


def delete_auction(auction_id, user_Key):
    print("Delete Auction:")
    print("Auction ID to be deleted:", auction_id)
    request = f"DELETE_AUCTION:{auction_id}"
    response = send_request(request, user_Key)

    if response is None:
        print("No response received from the server.")
    else:
        print("Deletion :", response.encode())


if __name__ == '__main__':
    userKey = getting_key()
    # Display menu options
    while True:
        print("\n$$$$$$$$$$$$$$$$$$$  AUCTION MANAGEMENT SYSTEM   $$$$$$$$$$$$$$$$$$$$$$")
        print("\nPlease Select One  Options:")
        print("1. Register User")
        print("2. Login and Create Auction")
        print("3. Place Bid")
        print("4. Display Auction Status")
        print("5. Display user")
        print("6. Modify Auction")
        print("7. Delete Auction")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            response_register = register_user(userKey)
            print("Registration :", response_register)
        elif choice == '2':
            print("Login")
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_response = login(username, password, userKey)
            print("Login :", login_response)
            response_auction = create_auction(userKey)
            print("Auction Creation :", response_auction)
        elif choice == '3':
            response_place_bid = place_bid(userKey)
            print("Bid Placement Successfully!!:", response_place_bid)
        elif choice == '4':
            response_display_status = display_auction_status(userKey)
            print("Auction Status For", response_display_status)
        elif choice == '5':
            display_all_users(userKey)
        elif choice == '6':
            modify_auction(userKey)
        elif choice == '7':
            auction_id = input("Enter auction ID to delete: ")
            delete_auction(auction_id, userKey)
        elif choice == '8':
            print("Exiting the client.")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-8).")
