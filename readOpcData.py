import json
import requests
from opcua import Client

def send_data_to_container(container_url, json_data):
    try:
        # Send a POST request with the JSON data
        response = requests.post(container_url, json=json_data)
        print("Response from Container B:", response.text)
    except requests.ConnectionError:
        print("Error: Connection to Container B failed. Container B may not be running or the URL may be incorrect.")
    except Exception as e:
        print("Error sending data to Container B:", e)


def browse_opc_nodes(config_data):
    def browse_node_recursive(node, result, level=0):
        # Browse the children of the current node recursively
        for child_node in node.get_children():
            # Check if the node is of type 'Variable'
            if child_node.get_node_class().name == "Variable":
                # Print the display name of the variable and its value
                try:
                    value = child_node.get_value()
                    result[child_node.get_display_name().Text] = value
                except Exception as e:
                    result[child_node.get_display_name().Text] = str(e)
            else:
                # Recursively browse the children of the child node if it's not a variable
                browse_node_recursive(child_node, result, level + 1)

    def get_display_name_for_node(client, node_id):
        try:
            node = client.get_node(node_id)
            display_name = node.get_display_name().Text
            return display_name
        except Exception as e:
            print(f"Error getting display name for NodeId {node_id}: {e}")
            return None

    # Connect to the OPC UA server
    client = Client(config_data[0]["EndpointUrl"])

    try:
        client.connect()
        print(f"Connected to {config_data[0]['EndpointUrl']} successfully!")

        while True:
            try:
                # Loop through each server configuration
                for server_config in config_data:
                    container_url = server_config["ContainerUrl"]
                    # Iterate over the nodes in the server configuration and browse their variables
                    for opc_node in server_config["OpcNodes"]:
                        node_id = opc_node["Id"]
                        # Get display name for NodeId
                        display_name = get_display_name_for_node(client, node_id)
                        if display_name:
                            print(f"Browsing node: {display_name}")
                            result = {"NodeName": display_name}
                            browse_node_recursive(client.get_node(node_id), result)
                            # Convert result to JSON and print
                            result_json = json.dumps(result, indent=4)
                            print(result_json)
                            send_data_to_container(container_url, result_json)

            except KeyboardInterrupt:
                print("Script interrupted by user. Exiting...")
                break

            except Exception as e:
                print("An error occurred:", e)

    finally:
        # Disconnect from the server
        client.disconnect()
        print(f"Disconnected from {config_data[0]['EndpointUrl']}")

    print("Script exiting...")

if __name__ == "__main__":
    # Read the JSON file
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    
    browse_opc_nodes(config_data)
