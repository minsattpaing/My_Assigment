# Import your encryption and decryption classes
from s_ecrypt_decrypt import CustomEncryption, CustomDecryption
import socket
import json

# Create instances of encryption and decryption classes
custom_encryption = CustomEncryption()
custom_decryption = CustomDecryption()

# Constants for file names
USERS_FILE = 'users.txt'
AUCTIONS_FILE = 'auctions.txt'


# Function to load data from a file
def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            data = file.read().strip()
            if data:
                return json.loads(data)
            else:
                return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []


# Function to save data to a file
def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


# Function to retrieve all users and auctions data
def get_all_users():
    users = load_data(USERS_FILE)
    return users


# User registration
def register_user(username, password, contact_details):
    users = load_data(USERS_FILE)
    new_user = {'username': username, 'password': password, 'contact_details': contact_details}
    users.append(new_user)
    save_data(users, USERS_FILE)
    return f"User '{username}' registered successfully!"


# Function for user login
def login_user(username, password):
    users = load_data(USERS_FILE)
    for user in users:
        if user['username'] == username and user['password'] == password:
            return "Login successful"
    return "Login failed. Invalid credentials"


# Function for auction creation
def create_auction(auction_id, title, description, end_time, username, password):
    login_result = login_user(username, password)
    if login_result == "Login successful":
        auctions = load_data(AUCTIONS_FILE)
        new_auction = {
            'auction_id': auction_id,
            'title': title,
            'description': description,
            'end_time': end_time,
            'highest_bid': 0,
            'highest_bidder': None
        }
        auctions.append(new_auction)
        save_data(auctions, AUCTIONS_FILE)
        return f"Auction '{title}' created successfully!"
    else:
        return "User authentication failed. Please log in to create an auction."


# Function to place a bid on an auction
def place_bid(auction_id, username, bid_amount):
    auctions = load_data(AUCTIONS_FILE)

    for auction in auctions:
        print(auction)
        if 'auction_id' in auction and auction['auction_id'] == auction_id:
            if auction['auction_id'] == auction_id:
                current_highest_bid = auction.get('highest_bid', 0)
                if bid_amount > current_highest_bid:
                    auction['highest_bid'] = bid_amount
                    auction['highest_bidder'] = username
                    save_data(auctions, AUCTIONS_FILE)
                    return f"Bid of {bid_amount} placed by {username} for Auction ID {auction_id}"
                else:
                    return "Your bid amount should be higher than the current highest bid."

            return f"Auction ID {auction_id} not found."


# Function to display auction status
def display_auction_status(auction_id):
    auctions = load_data(AUCTIONS_FILE)

    for auction in auctions:
        if auction.get('auction_id') == auction_id:
            response = f"Auction Status For Auction ID: {auction_id}\n"
            response += f"Title: {auction.get('title', 'N/A')}\n"
            response += f"Description: {auction.get('description', 'N/A')}\n"
            response += f"End Time: {auction.get('end_time', 'N/A')}\n"

            if auction.get('highest_bid', 0) == 0 or auction.get('highest_bidder') is None:
                response += "Highest Bid: No bids yet\n"
                response += "Highest Bidder: No bids yet\n"
            else:
                response += f"Highest Bid: {auction['highest_bid']}\n"
                response += f"Highest Bidder: {auction['highest_bidder']}\n"
            response += f"Details: {auction.get('details', 'No additional details')}\n"
            return response

    return f"Auction ID {auction_id} not found."


# Function to modify auction details
def modify_auction(auction_id, new_details):
    auctions = load_data(AUCTIONS_FILE)
    for auction in auctions:
        if auction['auction_id'] == auction_id:
            # Update the auction details with the new information
            auction['details'] = new_details
            save_data(auctions, AUCTIONS_FILE)  # Save the modified auctions back to the file
            return f"Auction ID {auction_id} has been modified with new details: {new_details}"

    # If auction ID not found, return a response indicating failure
    return f"Failed to modify. Auction ID {auction_id} not found."


# Function to delete an auction
def delete_auction(auction_id):
    if not auction_id.strip():
        return "Invalid Auction ID. Please provide a valid ID."

    auctions = load_data(AUCTIONS_FILE)
    found = False

    print("Auction IDs available for deletion:", [auction['auction_id'] for auction in auctions])

    for index, auction in enumerate(auctions):
        if 'auction_id' in auction and auction['auction_id'] == int(auction_id):
            del auctions[index]
            save_data(auctions, AUCTIONS_FILE)
            found = True
            break

    if found:
        return f"Auction ID {auction_id} deleted successfully."
    else:
        return f"Auction ID {auction_id} not found."


# Function to handle client requests
def handle_client_request(request):
    decrypted_request = custom_decryption.perform_decryption(request, "minsatt")

    # Handle empty or invalid data
    if not decrypted_request:
        return "Empty or invalid request data"

    try:
        request_parts = decrypted_request.split(':')

        if request_parts[0] == 'REGISTER' and len(request_parts) == 4:
            _, username, password, contact_details = request_parts
            return register_user(username, password, contact_details)

        elif request_parts[0] == 'LOGIN' and len(request_parts) == 3:
            _, username, password = request_parts
            return login_user(username, password)

        elif request_parts[0] == 'CREATE_AUCTION' and len(request_parts) == 7:
            _, auction_id, title, description, end_time, username, password = request_parts
            return create_auction(int(auction_id), title, description, end_time, username, password)

        elif request_parts[0] == 'PLACE_BID' and len(request_parts) == 4:
            _, auction_id, username, bid_amount = request_parts
            response = place_bid(int(auction_id), username, float(bid_amount))
            return response

        elif request_parts[0] == 'DISPLAY_AUCTION_STATUS' and len(request_parts) == 2:
            _, auction_id = request_parts
            response = display_auction_status(int(auction_id))
            return response

        elif request_parts[0] == 'MODIFY_AUCTION' and len(request_parts) >= 3:
            _, auction_id, new_details = request_parts
            return modify_auction(int(auction_id), new_details)

        elif request_parts[0] == 'DISPLAY_ALL_DATA' and len(request_parts) == 1:
            all_users = get_all_users()
            if all_users:
                return json.dumps({'users': all_users})
            else:
                return "No user or auction information available."

        elif request_parts[0] == 'DELETE_AUCTION' and len(request_parts) == 2:
            _, auction_id = request_parts
            response = delete_auction(auction_id)
            return response

        else:
            return "Invalid request format"

    except ValueError:
        return "ValueError occurred while processing request"
    except IndexError:
        return "IndexError occurred while processing request"
    except Exception as e:
        return f"Error occurred while processing request: {e}"


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9192))
    server.listen(5)
    print("Server is listening...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address} has been established.")

        encrypted_request = client_socket.recv(4096).decode()
        # Add this line to display the received request
        print("Received encrypted request:", encrypted_request)

        try:
            response = handle_client_request(encrypted_request)
        except Exception as e:
            response = f"Error processing request: {e}"

        encrypted_response = custom_encryption.perform_encryption(response, "minsatt")
        client_socket.send(encrypted_response.encode())
        client_socket.close()


if __name__ == "__main__":
    main()
